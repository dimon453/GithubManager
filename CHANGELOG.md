# Changelog

## v0.5 — Первый публичный релиз

### Новые функции

#### 🎨 Темы оформления
- **Светлая и тёмная тема** — переключение через кнопку ☀️/🌙 в шапке приложения
- Dark тема: `#0E0E0B` фон, `#AFE607` акценты (оригинальная)
- Light тема: `#F5F5F5` фон, `#8BC034` акценты
- Все элементы интерфейса полностью переокрашиваются при смене темы (Entry, Radiobutton, Checkbox, лог, прогресс-бар)

#### 📁 Drag-n-drop файлов
- Перетащи `.txt` файл прямо в поле для файла
- Или используй кнопку «Обзор» как раньше
- Требует: `tkinterdnd2>=0.3.0`

#### ✔️ Проверка токена
- Кнопка «Проверить» рядом с полем токена
- Быстрая валидация токена через GitHub API (GET /user)
- Зелёный результат ✓ если токен валидный, красный ✗ если истёк

#### ➕➖ Режим удаления collaborator'ов
- RadioButton переключатель: **Add** / **Delete**
- **Add** — добавляет пользователей с выбранным уровнем доступа (по умолчанию)
- **Delete** — удаляет пользователей из репозитория, поле permission скрывается
- В логе показываются статусы: "добавлено", "уже collaborator", "удалено", "не был collaborator'ом"

#### 📚 История репозиториев
- **Выпадающий список (Combobox)** для выбора репозитория вместо простого текстового поля
- Сохраняется до **10 последних использованных репозиториев** в `USERDATA.json`
- Автоматическое добавление в историю при успешном завершении операции (ok_count > 0)
- Без дубликатов — новый репо переходит в начало списка
- Удобный выбор: просто нажми на стрелку вниз и выбери из истории, или введи новый репо вручную

#### 🌍 Многоязычность
- Поддержка трёх языков: **RU** / **EN** / **RO**
- Быстрое переключение кнопками в шапке
- Все строки интерфейса, ошибки, статусы и логи переводятся мгновенно

#### 💾 Улучшенное сохранение данных
- `USERDATA.json` теперь хранит:
  - `github_username` — твой GitHub username
  - `github_token` — твой токен
  - `repo_history` — массив последних 10 репозиториев
- Данные синхронизируются с файлом при каждом значимом действии

### Исправления

- ✅ Полная переокраска всех элементов при смене темы (Entry, Radiobutton, Checkbox, Text, Scrollbar, Combobox)
- ✅ Корректная работа SSL сертификатов на macOS (через `certifi`)
- ✅ Правильная обработка username/репо с автоматическим обновлением префикса

### Технические детали

- **Главное окно:** `tkdnd.Tk` (вместо `tk.Tk`) для поддержки drag-n-drop
- **Combobox:** `ttk.Combobox` для историии репозиториев с переокраской при смене темы
- **Сохранение:** функция `add_to_repo_history()` управляет историей (max 10, без дубликатов)
- **Многопоточность:** все API-запросы и операции выполняются в отдельных потоках
- **Темизация:** централизованная система цветов `THEMES` позволяет легко добавлять новые темы

### Требования

```
certifi>=2024.0.0
tkinterdnd2>=0.3.0
```

Установка:
```bash
pip install -r requirements.txt
```

### Файлы проекта

- `add_collaborators_gui.py` — основное приложение (GUI версия)
- `add_collaborators.py` — CLI версия (интерактивный скрипт в терминале)
- `requirements.txt` — зависимости
- `USERDATA.json` — автоматически создаётся при первом запуске

### Известные ограничения

- Drag-n-drop работает только на `tkinterdnd2` (требует отдельную установку)
- На Windows может потребоваться разрешить запуск неподписанного `.exe` файла в Defender
- История репозиториев хранится в плотексте (обычный JSON), как и токен — храни `USERDATA.json` в безопасном месте

---

## План развития (для будущих версий)

- [ ] Drag-n-drop для multiple файлов
- [ ] Просмотр текущих collaborator'ов репозитория
- [ ] Синхронизация (добавить новых, удалить старых, обновить уровни в одном проходе)
- [ ] Работа с несколькими репозиториями одновременно
- [ ] Web-версия приложения (Flask)
- [ ] VS Code extension
- [ ] Шифрование токена в `USERDATA.json`
- [ ] Экспорт результатов в CSV/JSON

---

*Proudly made by Popov Dmitrii*

---

# Changelog

## v0.5 — First Public Release

### New Features

#### 🎨 Theme Customization
- **Light and Dark themes** — toggle with ☀️/🌙 button in the header
- Dark theme: `#0E0E0B` background, `#AFE607` accents (original)
- Light theme: `#F5F5F5` background, `#8BC034` accents
- All UI elements fully recolor on theme switch (Entry, Radiobutton, Checkbox, log, progress bar)

#### 📁 Drag-n-Drop Files
- Drag `.txt` file directly into the file field
- Or use the "Browse" button as before
- Requires: `tkinterdnd2>=0.3.0`

#### ✔️ Token Verification
- "Check" button next to token field
- Quick token validation via GitHub API (GET /user)
- Green ✓ result if token is valid, red ✗ if expired

#### ➕➖ Delete Collaborators Mode
- RadioButton toggle: **Add** / **Delete**
- **Add** — adds users with selected permission level (default)
- **Delete** — removes users from repository, permission field is hidden
- Log shows status: "added", "already collaborator", "removed", "was not collaborator"

#### 📚 Repository History
- **Dropdown list (Combobox)** for repository selection instead of plain text field
- Stores up to **10 most recent repositories** in `USERDATA.json`
- Auto-adds to history on successful operation (ok_count > 0)
- No duplicates — new repo moves to the top of the list
- Convenient selection: click the dropdown arrow or type a new repo

#### 🌍 Multilingual Support
- Three languages: **RU** / **EN** / **RO**
- Quick language switching with buttons in header
- All interface strings, errors, statuses, and logs translate instantly

#### 💾 Enhanced Data Saving
- `USERDATA.json` now stores:
  - `github_username` — your GitHub username
  - `github_token` — your token
  - `repo_history` — array of last 10 repositories
- Data syncs with file on each significant action

### Bug Fixes

- ✅ Full recolor of all elements on theme change (Entry, Radiobutton, Checkbox, Text, Scrollbar, Combobox)
- ✅ Proper SSL certificate handling on macOS (via `certifi`)
- ✅ Correct username/repo handling with automatic prefix updating

### Technical Details

- **Main window:** `tkdnd.Tk` (instead of `tk.Tk`) for drag-n-drop support
- **Combobox:** `ttk.Combobox` for repository history with theme recoloring
- **Saving:** `add_to_repo_history()` function manages history (max 10, no duplicates)
- **Threading:** all API calls and operations run in separate threads
- **Theming:** centralized `THEMES` color system makes adding new themes easy

### Requirements

```
certifi>=2024.0.0
tkinterdnd2>=0.3.0
```

Install:
```bash
pip install -r requirements.txt
```

### Project Files

- `add_collaborators_gui.py` — main application (GUI version)
- `add_collaborators.py` — CLI version (interactive terminal script)
- `requirements.txt` — dependencies
- `USERDATA.json` — auto-created on first run

### Known Limitations

- Drag-n-drop only works via `tkinterdnd2` (requires separate installation)
- On Windows, unsigned `.exe` file may require Windows Defender permission
- Repository history stored in plaintext (regular JSON), like the token — keep `USERDATA.json` secure

---

## Future Plans (for upcoming versions)

- [ ] Drag-n-drop for multiple files
- [ ] View current repository collaborators
- [ ] Sync mode (add new, remove old, update levels in one pass)
- [ ] Manage multiple repositories at once
- [ ] Web version (Flask)
- [ ] VS Code extension
- [ ] Token encryption in `USERDATA.json`
- [ ] Export results to CSV/JSON

---

*Proudly made by Popov Dmitrii*
