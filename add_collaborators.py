#!/usr/bin/env python3
"""
Добавляет пользователей GitHub в репозиторий как collaborator.
Параметры запрашиваются интерактивно по очереди.
Токен и имя пользователя сохраняются в USERDATA.json рядом со скриптом.
"""

import sys
import time
import urllib.request
import urllib.error
import json
import os
import ssl
import certifi

PERMISSION_CHOICES = ("pull", "push", "maintain", "triage", "admin")
USERDATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "USERDATA.json")
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


# ── helpers ───────────────────────────────────────────────────────────────────

def ask(prompt: str, default: str = "") -> str:
    while True:
        hint = f" [{default}]" if default else ""
        value = input(f"{prompt}{hint}: ").strip()
        if value:
            return value
        if default:
            return default
        print("  Поле не может быть пустым, попробуй ещё раз.")


def ask_yn(prompt: str) -> bool:
    return input(prompt + " (y/n): ").strip().lower() in ("y", "yes", "д", "да")


# ── USERDATA ──────────────────────────────────────────────────────────────────

def load_userdata() -> dict:
    if os.path.isfile(USERDATA_FILE):
        try:
            with open(USERDATA_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_userdata(data: dict):
    with open(USERDATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Сохранено в {USERDATA_FILE}")


# ── GitHub API ────────────────────────────────────────────────────────────────

def add_collaborator(owner, repo, username, token, permission) -> dict:
    url = f"https://api.github.com/repos/{owner}/{repo}/collaborators/{username}"
    payload = json.dumps({"permission": permission}).encode()
    req = urllib.request.Request(
        url,
        data=payload,
        method="PUT",
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


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    print("=== GitHub Collaborator Adder ===\n")

    userdata    = load_userdata()
    saved_user  = userdata.get("github_username", "")
    saved_token = userdata.get("github_token", "")

    # 1. Путь к файлу
    while True:
        file_path = ask("Путь к txt-файлу с никами")
        if os.path.isfile(file_path):
            break
        print(f"  Файл '{file_path}' не найден, попробуй ещё раз.")

    with open(file_path, encoding="utf-8") as f:
        usernames = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    if not usernames:
        print("Файл пуст или не содержит ников.")
        sys.exit(1)

    print(f"  Найдено пользователей: {len(usernames)}\n")

    # 2. Репозиторий
    while True:
        repo_input = ask("Репозиторий (формат OWNER/REPO)")
        parts = repo_input.split("/")
        if len(parts) == 2 and all(parts):
            owner, repo = parts
            break
        print("  Неверный формат, нужно OWNER/REPO (например, myorg/myrepo).")

    # 3. Имя пользователя GitHub
    gh_user = ask("Твой GitHub username", default=saved_user)

    # 4. Токен
    token = ask("GitHub Token", default=saved_token)

    # Предложить сохранить, если данные новые
    if gh_user != saved_user or token != saved_token:
        if ask_yn("\nСохранить username и токен в USERDATA.json?"):
            save_userdata({"github_username": gh_user, "github_token": token})

    print()

    # 5. Уровень доступа
    choices_str = " / ".join(PERMISSION_CHOICES)
    while True:
        perm = ask(f"Уровень доступа [{choices_str}]", default="push")
        if perm in PERMISSION_CHOICES:
            break
        print(f"  Допустимые значения: {choices_str}")

    # Подтверждение
    print(f"\n  Репозиторий  : {owner}/{repo}")
    print(f"  Разрешение   : {perm}")
    print(f"  Пользователей: {len(usernames)}")
    if not ask_yn("\nПродолжить?"):
        print("Отменено.")
        sys.exit(0)

    print()
    ok_count = 0
    fail_count = 0

    for username in usernames:
        result = add_collaborator(owner, repo, username, token, perm)
        if result["ok"]:
            tag = "приглашение отправлено" if result["status"] == 201 else "уже collaborator"
            print(f"  ✓  {username:<30}  [{result['status']}] {tag}")
            ok_count += 1
        else:
            try:
                msg = json.loads(result["body"]).get("message", result["body"])
            except Exception:
                msg = result["body"]
            print(f"  ✗  {username:<30}  [{result['status']}] {msg}")
            fail_count += 1
        time.sleep(0.3)

    print(f"\nГотово: {ok_count} успешно, {fail_count} ошибок.")


if __name__ == "__main__":
    main()