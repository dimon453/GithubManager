#!/usr/bin/env python3
"""
GitHub Collaborator Adder — GUI (tkinter)
Цветовая схема: фон, акцент, с поддержкой светлой/тёмной темы
Языки: RU / EN / RO
Функции: drag-n-drop, проверка токена, удаление collaborator'ов, светлая/тёмная тема
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
import tkinterdnd2 as tkdnd

# ── константы ─────────────────────────────────────────────────────────────────

THEMES = {
    "dark": {
        "bg":       "#0E0E0B",
        "accent":   "#AFE607",
        "fg":       "#E8E8E8",
        "bg2":      "#1A1A16",
        "bg3":      "#252520",
        "red":      "#FF4C4C",
        "muted":    "#555550",
        "entry_bg": "#252520",
        "entry_fg": "#E8E8E8",
    },
    "light": {
        "bg":       "#F5F5F5",
        "accent":   "#8BC034",
        "fg":       "#1A1A1A",
        "bg2":      "#E8E8E8",
        "bg3":      "#D0D0D0",
        "red":      "#D32F2F",
        "muted":    "#999999",
        "entry_bg": "#FFFFFF",
        "entry_fg": "#1A1A1A",
    },
}

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
        "lbl_mode":     "Режим",
        "btn_browse":   "Обзор",
        "btn_check":    "Проверить",
        "btn_run":      "▶  Выполнить",
        "btn_add":      "Добавить",
        "btn_delete":   "Удалить",
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
        "log_deleted":  "успешно удалён",
        "log_not_found":"не был collaborator'ом",
        "log_done":     "Готово: {} успешно, {} ошибок.",
        "log_checking": "Проверка токена...",
        "log_valid":    "✓ Токен валидный",
        "log_invalid":  "✗ Токен невалидный или истёк",
        "footer":       "Proudly made by Popov Dmitrii",
    },
    "EN": {
        "title":        "GitHub Collaborator Adder",
        "lbl_file":     "Usernames file",
        "lbl_repo":     "Repository (OWNER/REPO)",
        "lbl_user":     "GitHub Username",
        "lbl_token":    "GitHub Token",
        "lbl_perm":     "Permission",
        "lbl_mode":     "Mode",
        "btn_browse":   "Browse",
        "btn_check":    "Check",
        "btn_run":      "▶  Run",
        "btn_add":      "Add",
        "btn_delete":   "Delete",
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
        "log_deleted":  "successfully removed",
        "log_not_found":"was not a collaborator",
        "log_done":     "Done: {} succeeded, {} failed.",
        "log_checking": "Checking token...",
        "log_valid":    "✓ Token is valid",
        "log_invalid":  "✗ Token is invalid or expired",
        "footer":       "Proudly made by Popov Dmitrii",
    },
    "RO": {
        "title":        "GitHub Collaborator Adder",
        "lbl_file":     "Fișier cu utilizatori",
        "lbl_repo":     "Depozit (OWNER/REPO)",
        "lbl_user":     "Nume utilizator GitHub",
        "lbl_token":    "Token GitHub",
        "lbl_perm":     "Permisiune",
        "lbl_mode":     "Mod",
        "btn_browse":   "Răsfoire",
        "btn_check":    "Verifica",
        "btn_run":      "Executa",
        "btn_add":      "Adauga",
        "btn_delete":   "Sterge",
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
        "log_deleted":  "eliminat cu succes",
        "log_not_found":"nu era colaborator",
        "log_done":     "Gata: {} reușite, {} eșuate.",
        "log_checking": "Se verifică tokenul...",
        "log_valid":    "✓ Token valid",
        "log_invalid":  "✗ Token invalid sau expirat",
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

def save_userdata(username: str, token: str, repo_history: list = None):
    data = {"github_username": username, "github_token": token}
    if repo_history:
        data["repo_history"] = repo_history
    with open(USERDATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_to_repo_history(repo: str, history: list) -> list:
    """Добавить репо в историю (max 10, без дубликатов, в начало)."""
    if not repo or "/" not in repo:
        return history
    # Убрать дубликаты
    history = [r for r in history if r != repo]
    # Добавить в начало и ограничить до 10
    history.insert(0, repo)
    return history[:10]

# ── GitHub API ────────────────────────────────────────────────────────────────

def check_token(token: str) -> bool:
    """Проверить валидность токена."""
    try:
        url = "https://api.github.com/user"
        req = urllib.request.Request(
            url,
            headers={"Authorization": f"Bearer {token}"},
        )
        with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False

def add_collaborator(owner, repo, username, token, permission) -> dict:
    """Добавить collaborator."""
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

def delete_collaborator(owner, repo, username, token) -> dict:
    """Удалить collaborator."""
    url = f"https://api.github.com/repos/{owner}/{repo}/collaborators/{username}"
    req = urllib.request.Request(
        url, method="DELETE",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, context=SSL_CONTEXT) as resp:
            return {"status": resp.status, "ok": True}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "ok": False, "body": e.read().decode()}

# ── GUI ───────────────────────────────────────────────────────────────────────

class App(tkdnd.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "RU"
        self.theme = "dark"
        self.resizable(False, False)
        self.userdata = load_userdata()
        self.repo_history = self.userdata.get("repo_history", [])
        self.entries = []
        self.radios = []
        self.frames = []
        self._build_ui()
        self._load_saved()
        self._apply_theme_and_lang()

    def t(self, key, *args):
        s = STRINGS[self.lang][key]
        return s.format(*args) if args else s

    def color(self, key):
        return THEMES[self.theme][key]

    # ── стили ─────────────────────────────────────────────────────────────────

    def _entry(self, parent, textvariable):
        e = tk.Entry(
            parent, textvariable=textvariable,
            relief="flat", font=("Segoe UI", 10),
            highlightthickness=1,
        )
        self.entries.append(e)
        return e

    def _label(self, parent, text="", bold=False):
        return tk.Label(parent, text=text, 
                        font=("Segoe UI", 10, "bold") if bold else ("Segoe UI", 10))

    def _btn(self, parent, text, cmd, small=False):
        return tk.Button(
            parent, text=text, command=cmd,
            activeforeground=self.color("bg"),
            font=("Segoe UI", 10, "bold") if not small else ("Segoe UI", 10),
            relief="flat", cursor="hand2",
            padx=10 if not small else 6, pady=4,
        )

    # ── построение UI ─────────────────────────────────────────────────────────

    def _build_ui(self):
        pad = {"padx": 20, "pady": 6}

        # — шапка —
        header = tk.Frame(self)
        self.frames.append(("header", header))
        header.pack(fill="x", padx=20, pady=(18, 2))

        self.lbl_title = tk.Label(header, text="", font=("Segoe UI", 13, "bold"))
        self.lbl_title.pack(side="left")

        # кнопки языков + темы
        ctrl_frame = tk.Frame(header)
        self.frames.append(("ctrl", ctrl_frame))
        ctrl_frame.pack(side="right")
        self.lang_btns = {}
        for lang in ("RU", "EN", "RO"):
            b = tk.Button(
                ctrl_frame, text=lang, width=3, relief="flat", cursor="hand2",
                font=("Segoe UI", 10, "bold"),
                command=lambda l=lang: self._switch_lang(l),
            )
            b.pack(side="left", padx=2)
            self.lang_btns[lang] = b
        
        self.theme_btn = tk.Button(
            ctrl_frame, text="🌙", width=3, relief="flat", cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            command=self._switch_theme,
        )
        self.theme_btn.pack(side="left", padx=2)

        self.separator = tk.Frame(self, height=2)
        self.frames.append(("sep", self.separator))
        self.separator.pack(fill="x", padx=20, pady=(4, 10))

        # — форма —
        form = tk.Frame(self)
        self.frames.append(("form", form))
        form.pack(fill="x", **pad)
        form.columnconfigure(1, weight=1)

        # файл
        self.lbl_file = self._label(form)
        self.lbl_file.grid(row=0, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_file = tk.StringVar()
        file_frame = tk.Frame(form)
        self.frames.append(("file_frame", file_frame))
        file_frame.grid(row=0, column=1, sticky="ew", pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.file_entry = self._entry(file_frame, self.var_file)
        self.file_entry.grid(row=0, column=0, sticky="ew", ipady=4)
        # Регистрация drop target
        self.file_entry.drop_target_register(tkdnd.DND_FILES)
        self.file_entry.dnd_bind('<<Drop>>', self._on_file_drop)
        
        self.btn_browse = self._btn(file_frame, "", self._browse, small=True)
        self.btn_browse.grid(row=0, column=1, padx=(6, 0))

        # репозиторий
        self.lbl_repo = self._label(form)
        self.lbl_repo.grid(row=1, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_repo = tk.StringVar()
        self.repo_combo = ttk.Combobox(
            form, textvariable=self.var_repo,
            state="normal", font=("Segoe UI", 10)
        )
        self.repo_combo.grid(row=1, column=1, sticky="ew", ipady=4, pady=5)

        # username
        self.lbl_user = self._label(form)
        self.lbl_user.grid(row=2, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_user = tk.StringVar()
        user_entry = self._entry(form, self.var_user)
        user_entry.grid(row=2, column=1, sticky="ew", ipady=4, pady=5)
        self.var_user.trace_add("write", self._on_user_change)

        # токен
        self.lbl_token = self._label(form)
        self.lbl_token.grid(row=3, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_token = tk.StringVar()
        token_frame = tk.Frame(form)
        self.frames.append(("token_frame", token_frame))
        token_frame.grid(row=3, column=1, sticky="ew", pady=5)
        token_frame.columnconfigure(0, weight=1)
        self._entry(token_frame, self.var_token).grid(row=0, column=0, sticky="ew", ipady=4)
        self.btn_check = self._btn(token_frame, "", self._check_token, small=True)
        self.btn_check.grid(row=0, column=1, padx=(6, 0))

        # режим (Add/Delete)
        self.lbl_mode = self._label(form)
        self.lbl_mode.grid(row=4, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_mode = tk.StringVar(value="add")
        mode_frame = tk.Frame(form)
        self.frames.append(("mode_frame", mode_frame))
        mode_frame.grid(row=4, column=1, sticky="w", pady=5)
        
        for text, value in [("Add", "add"), ("Delete", "delete")]:
            r = tk.Radiobutton(
                mode_frame, text=text, variable=self.var_mode, value=value,
                font=("Segoe UI", 10), command=self._on_mode_change,
            )
            r.pack(side="left", padx=(0, 15) if value == "add" else 0)
            self.radios.append(r)

        # permission (скрывается при Delete)
        self.lbl_perm = self._label(form)
        self.lbl_perm.grid(row=5, column=0, sticky="w", padx=(0, 12), pady=5)
        self.var_perm = tk.StringVar(value="push")
        self.perm_frame = tk.Frame(form)
        self.frames.append(("perm_frame", self.perm_frame))
        self.perm_frame.grid(row=5, column=1, sticky="w", pady=5)
        for p in PERMISSION_CHOICES:
            r = tk.Radiobutton(
                self.perm_frame, text=p, variable=self.var_perm, value=p,
                font=("Segoe UI", 10),
            )
            r.pack(side="left", padx=(0, 10))
            self.radios.append(r)

        # чекбокс сохранить
        self.var_save = tk.BooleanVar(value=True)
        self.chk_save = tk.Checkbutton(self, variable=self.var_save, font=("Segoe UI", 10))
        self.chk_save.pack(anchor="w", padx=20, pady=(0, 4))

        # кнопка запуска
        self.btn_run = self._btn(self, "", self._run)
        self.btn_run.pack(fill="x", padx=20, pady=(4, 10), ipady=6)

        # прогресс-бар
        self.progress = ttk.Progressbar(self, mode="determinate", length=400)
        style = ttk.Style(self)
        style.theme_use("clam")
        self.progress.pack(fill="x", padx=20, pady=(0, 6))

        # лог
        log_frame = tk.Frame(self, highlightthickness=1)
        self.frames.append(("log_frame", log_frame))
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        self.log_frame = log_frame
        self.log = tk.Text(
            log_frame, font=("Consolas", 9),
            relief="flat", state="disabled", wrap="word", height=12,
        )
        sb = tk.Scrollbar(log_frame, command=self.log.yview, relief="flat")
        self.log.configure(yscrollcommand=sb.set)
        self.log.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        sb.pack(side="right", fill="y")
        self.log.tag_config("ok",      font=("Consolas", 9))
        self.log.tag_config("err",     font=("Consolas", 9))
        self.log.tag_config("info",    font=("Consolas", 9))
        self.log.tag_config("heading", font=("Consolas", 9, "bold"))

        # футер
        self.lbl_footer = tk.Label(self, text="", font=("Segoe UI", 8))
        self.lbl_footer.pack(pady=(0, 10))

    # ── язык и тема ───────────────────────────────────────────────────────────

    def _switch_lang(self, lang):
        self.lang = lang
        self._apply_theme_and_lang()

    def _switch_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self._apply_theme_and_lang()

    def _apply_theme_and_lang(self):
        # Основные цвета
        self.configure(bg=self.color("bg"))
        
        # Все фреймы
        for name, frame in self.frames:
            frame.configure(bg=self.color("bg"))
        
        # Все Entry
        for entry in self.entries:
            entry.configure(
                bg=self.color("entry_bg"),
                fg=self.color("entry_fg"),
                insertbackground=self.color("accent"),
                highlightcolor=self.color("accent"),
                highlightbackground="#333330",
            )
        
        # Combobox
        style = ttk.Style(self)
        style.configure("TCombobox",
                        fieldbackground=self.color("entry_bg"),
                        background=self.color("entry_bg"),
                        foreground=self.color("entry_fg"))
        self.repo_combo.configure(style="TCombobox")
        
        # Все Radiobutton'ы и Checkbox
        for radio in self.radios:
            radio.configure(
                bg=self.color("bg"),
                fg=self.color("fg"),
                selectcolor=self.color("bg2"),
                activebackground=self.color("bg"),
                activeforeground=self.color("accent"),
            )
        
        self.chk_save.configure(
            bg=self.color("bg"),
            fg=self.color("fg"),
            selectcolor=self.color("bg2"),
            activebackground=self.color("bg"),
            activeforeground=self.color("accent"),
        )
        
        # Лог
        self.log.configure(
            bg=self.color("bg2"),
            fg=self.color("fg"),
            insertbackground=self.color("accent"),
        )
        self.log.tag_config("ok",      foreground=self.color("accent"))
        self.log.tag_config("err",     foreground=self.color("red"))
        self.log.tag_config("info",    foreground=self.color("fg"))
        self.log.tag_config("heading", foreground=self.color("accent"))
        
        # Кнопки
        self.btn_browse.configure(bg=self.color("accent"), fg=self.color("bg"))
        self.btn_check.configure(bg=self.color("accent"), fg=self.color("bg"))
        self.btn_run.configure(bg=self.color("accent"), fg=self.color("bg"))
        self.theme_btn.configure(bg=self.color("bg3"), fg=self.color("fg"))
        
        # Разделитель
        self.separator.configure(bg=self.color("accent"))
        
        # Лог фрейм
        self.log_frame.configure(
            bg=self.color("bg"),
            highlightbackground=self.color("accent"),
        )
        
        # Scrollbar
        for child in self.log.master.children.values():
            if isinstance(child, tk.Scrollbar):
                child.configure(bg=self.color("bg3"), troughcolor=self.color("bg3"))
        
        # Заголовок
        self.lbl_title.configure(
            text=self.t("title"),
            bg=self.color("bg"),
            fg=self.color("accent"),
        )
        
        # Лейблы
        self.lbl_file.configure(text=self.t("lbl_file"), bg=self.color("bg"), fg=self.color("accent"))
        self.lbl_repo.configure(text=self.t("lbl_repo"), bg=self.color("bg"), fg=self.color("accent"))
        self.lbl_user.configure(text=self.t("lbl_user"), bg=self.color("bg"), fg=self.color("fg"))
        self.lbl_token.configure(text=self.t("lbl_token"), bg=self.color("bg"), fg=self.color("accent"))
        self.lbl_perm.configure(text=self.t("lbl_perm"), bg=self.color("bg"), fg=self.color("accent"))
        self.lbl_mode.configure(text=self.t("lbl_mode"), bg=self.color("bg"), fg=self.color("accent"))
        
        # Кнопки управления
        self.btn_browse.configure(text=self.t("btn_browse"))
        self.btn_check.configure(text=self.t("btn_check"))
        self.btn_run.configure(text=self.t("btn_run"))
        
        # Theme button
        self.theme_btn.configure(text="☀️" if self.theme == "dark" else "🌙")
        
        # Языки
        for lang, btn in self.lang_btns.items():
            if lang == self.lang:
                btn.configure(bg=self.color("accent"), fg=self.color("bg"))
            else:
                btn.configure(bg=self.color("bg3"), fg=self.color("fg"))
        
        # Чекбокс текст
        self.chk_save.configure(text=self.t("chk_save"))
        self.lbl_footer.configure(
            text=self.t("footer"),
            bg=self.color("bg"),
            fg=self.color("muted"),
        )
        
        # Прогресс-бар
        style = ttk.Style(self)
        style.configure("TProgressbar",
                        troughcolor=self.color("bg3"),
                        background=self.color("accent"),
                        bordercolor=self.color("bg"),
                        lightcolor=self.color("accent"),
                        darkcolor=self.color("accent"))

    # ── события ───────────────────────────────────────────────────────────────

    def _on_file_drop(self, event):
        """Обработка перетаскивания файла."""
        # tkinterdnd2 возвращает пути в фигурных скобках: {/path/to/file}
        files = event.data
        if files:
            # Убираем фигурные скобки и берём первый файл
            files = files.strip('{}').split()
            if files:
                self.var_file.set(files[0])

    def _on_user_change(self, *_):
        """Обновлять префикс репозитория при изменении username."""
        user = self.var_user.get().strip()
        repo = self.var_repo.get()
        if "/" in repo:
            after_slash = repo.split("/", 1)[1]
        else:
            after_slash = ""
        self.var_repo.set((user + "/" + after_slash) if user else after_slash)

    def _load_saved(self):
        saved_user = self.userdata.get("github_username", "")
        self.var_user.set(saved_user)
        self.var_token.set(self.userdata.get("github_token", ""))
        # Заполнить Combobox историей репозиториев
        self.repo_combo['values'] = self.repo_history
        # Подставить username/ в поле репозитория
        if saved_user:
            self.var_repo.set(saved_user + "/")
        user = self.var_user.get().strip()
        repo = self.var_repo.get()
        if "/" in repo:
            after_slash = repo.split("/", 1)[1]
        else:
            after_slash = ""
        self.var_repo.set((user + "/" + after_slash) if user else after_slash)

    def _on_mode_change(self):
        mode = self.var_mode.get()
        if mode == "delete":
            self.perm_frame.grid_remove()
        else:
            self.perm_frame.grid()

    def _browse(self):
        path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if path:
            self.var_file.set(path)

    def _check_token(self):
        token = self.var_token.get().strip()
        if not token:
            self._log("⚠  " + self.t("err_notoken"), "err")
            return
        self._log(self.t("log_checking"), "info")
        threading.Thread(target=self._check_token_worker, args=(token,), daemon=True).start()

    def _check_token_worker(self, token):
        time.sleep(0.5)
        if check_token(token):
            self._log(self.t("log_valid"), "ok")
        else:
            self._log(self.t("log_invalid"), "err")

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
        mode      = self.var_mode.get()

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
            save_userdata(gh_user, token, self.repo_history)
            self.userdata = {"github_username": gh_user, "github_token": token, 
                            "repo_history": self.repo_history}

        threading.Thread(
            target=self._worker,
            args=(owner, repo, token, perm, usernames, mode),
            daemon=True,
        ).start()

    def _worker(self, owner, repo, token, perm, usernames, mode):
        self._log_clear()
        self._log(self.t("log_repo", owner, repo), "heading")
        if mode == "add":
            self._log(self.t("log_perm", perm), "heading")
        self._log(self.t("log_total", len(usernames)) + "\n", "heading")

        self.progress["maximum"] = len(usernames)
        self.progress["value"]   = 0

        ok_count = fail_count = 0

        for i, username in enumerate(usernames, 1):
            if mode == "add":
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
            else:  # delete
                result = delete_collaborator(owner, repo, username, token)
                if result["ok"]:
                    self._log(f"  ✓  {username:<28}  [{result['status']}] {self.t('log_deleted')}", "ok")
                    ok_count += 1
                else:
                    body = result.get("body", "")
                    try:
                        msg = json.loads(body).get("message", body)
                    except Exception:
                        msg = "404" if result["status"] == 404 else body
                    tag_text = self.t("log_not_found") if result["status"] == 404 else msg
                    self._log(f"  ✗  {username:<28}  [{result['status']}] {tag_text}", "err")
                    fail_count += 1

            self.progress["value"] = i
            time.sleep(0.3)

        self._log("\n" + self.t("log_done", ok_count, fail_count), "heading")
        
        # Добавить репо в историю при успешном выполнении
        if ok_count > 0:
            repo_full = f"{owner}/{repo}"
            self.repo_history = add_to_repo_history(repo_full, self.repo_history)
            self.repo_combo['values'] = self.repo_history
            # Сохранить обновленную историю
            gh_user = self.var_user.get().strip()
            token = self.var_token.get().strip()
            save_userdata(gh_user, token, self.repo_history)


if __name__ == "__main__":
    app = App()
    app.mainloop()
