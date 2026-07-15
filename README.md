# GitHub Collaborator Adder
![GitHub Collaborator Adder](icon_256x256.png)

> 🇷🇴 [Versiunea în limba română](#github-collaborator-adder-ro)

Инструмент для массового добавления пользователей GitHub в репозиторий в роли collaborator. Доступен в двух версиях: консольный скрипт и графический интерфейс с поддержкой светлой/тёмной темы.

**Версия:** 1.0 | **Лицензия:** MIT | **Автор:** Popov Dmitrii

---

## 📚 Документация

- **[CHANGELOG.md](CHANGELOG.md)** — полный список изменений и новых функций
- **[RELEASE_NOTES.md](RELEASE_NOTES.md)** — краткая заметка к релизу

---

## Запуск скомпилированной версии под Windows

Если вы не хотите устанавливать Python, воспользуйтесь готовым исполняемым файлом `.exe`, который уже включён в репозиторий.

Загрузите файл `add_collaborators_gui.exe` со страницы релиза: [**версия 1.0**](https://github.com/OWNER/REPO/releases/tag/v1.0)

После загрузки поместите `add_collaborators_gui.exe` в удобную папку. При первом запуске рядом автоматически создастся файл `USERDATA.json` для хранения ваших данных. Никакая установка не требуется — достаточно дважды щёлкнуть по файлу.

> **Обратите внимание:** Windows Defender или другой антивирус может показать предупреждение при первом запуске — это стандартное поведение для неподписанных `.exe` файлов. Нажмите «Подробнее» → «Выполнить в любом случае» для продолжения.

---

## Файлы проекта

| Файл | Описание |
|---|---|
| `add_collaborators_gui.py` | GUI версия — графический интерфейс (tkinter) |
| `add_collaborators.py` | CLI версия — интерактивные вопросы в терминале |
| `add_collaborators_gui.exe` | Скомпилированная версия для Windows |
| `USERDATA.json` | Создаётся автоматически — хранит username, токен и историю репо |
| `requirements.txt` | Список зависимостей |
| `README.md` | Этот файл (документация) |
| `CHANGELOG.md` | Все изменения и улучшения |
| `RELEASE_NOTES.md` | Краткая заметка к релизу |

---

## Требования (для запуска из исходного кода)

Python 3.8+ и две внешние библиотеки:

```bash
pip install -r requirements.txt
```

Или вручную:

```bash
pip install certifi tkinterdnd2
```

Всё остальное входит в стандартную библиотеку Python.

---

## Формат входного файла

Обычный `.txt` файл, один GitHub-ник на каждой строке:

```
octocat
torvalds
# строки начинающиеся с # игнорируются
someuser
```

---

## CLI версия — `add_collaborators.py`

<details>
<summary>Показать инструкцию</summary>

Запуск:

```bash
python add_collaborators.py
```

Скрипт задаёт вопросы по очереди:

1. Путь к `.txt` файлу с никами
2. Репозиторий в формате `OWNER/REPO`
3. Ваш GitHub username
4. Ваш GitHub токен
5. Уровень доступа (`pull` / `push` / `maintain` / `triage` / `admin`)

Если username или токен отличаются от сохранённых — будет предложено обновить `USERDATA.json`.

</details>

---

## GUI версия — `add_collaborators_gui.py`

<details>
<summary>Показать инструкцию</summary>

Запуск:

```bash
python add_collaborators_gui.py
```

### Основные возможности

**Интерфейс:**
- Тёмная и светлая тема (кнопка ☀️/🌙) — фон `#0E0E0B`/`#F5F5F5`, акценты `#AFE607`/`#8BC034`
- Три языка: **RU** / **EN** / **RO** (мгновенное переключение)
- Профессиональный дизайн с контрастной палитрой

**Работа с файлами и репо:**
- Drag-n-drop файлов — перетащи `.txt` файл прямо в поле, или используй кнопку «Обзор»
- История репозиториев — выпадающий список с последними 10 использованными репо
- Username и токен загружаются автоматически из `USERDATA.json` при старте
- Поле репозитория заполняется как `username/` — необходимо только дописать название репо
- При изменении username префикс в поле репозитория обновляется автоматически

**Операции:**
- Проверка токена — кнопка «Проверить» рядом с полем токена (быстрая валидация через GitHub API)
- Два режима работы:
  - **Add** — добавляет пользователей с выбранным уровнем доступа (по умолчанию)
  - **Delete** — удаляет пользователей из репозитория (поле permission скрывается)
- Выбор уровня доступа через радиокнопки (только для режима Add)

**Мониторинг:**
- Лог с цветным выводом в реальном времени (зелёный — успех, красный — ошибка, жёлтый — информация)
- Прогресс-бар отслеживает ход выполнения операции
- Детальный статус для каждого пользователя (номер операции, результат)

**Сохранение данных:**
- Чекбокс для сохранения username и токена в `USERDATA.json`
- История репозиториев автоматически сохраняется при успешном завершении
- Синхронизация данных происходит мгновенно

</details>

---

## Как получить GitHub токен

1. Перейдите в **GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)**
2. Нажмите **Generate new token**
3. Укажите scope: `repo` (приватные репозитории) или `public_repo` (только публичные)
4. Скопируйте токен — он отображается только один раз

Прямая ссылка: https://github.com/settings/tokens/new

---

## Уровни доступа

| Уровень | Описание |
|---|---|
| `pull` | Только чтение |
| `push` | Чтение и запись (по умолчанию) |
| `maintain` | Управление репозиторием без доступа к настройкам |
| `triage` | Управление issues и pull request'ами |
| `admin` | Полный доступ включая настройки |

---

## USERDATA.json

Сохраняется автоматически при подтверждении. Находится в той же папке, что и скрипт или `.exe` файл.

```json
{
  "github_username": "ваш_ник",
  "github_token": "ghp_xxxxxxxxxxxx",
  "repo_history": ["owner1/repo1", "owner2/repo2"]
}
```

> **Храните этот файл в безопасном месте** — он содержит ваш GitHub токен.

---

## Примечания

- Между API-запросами выдерживается пауза 300 мс — чтобы не превышать rate limit GitHub
- Пользователи, которые уже являются collaborator'ами, получат обновлённый уровень доступа без ошибок (статус `204`)
- Новые пользователи получат приглашение, которое необходимо принять (статус `201`)
- Ошибка `401` означает, что токен недействителен или истёк — сгенерируйте новый
- История репо хранится локально и ограничена 10 последними репозиториями

---

## Известные проблемы и решения

### SSL ошибка при запуске
**Решение:** Установите certifi:
```bash
pip install certifi
```

### Tkinterdnd2 не установлена
**Решение:** Используйте кнопку Browse вместо drag-n-drop или установите:
```bash
pip install tkinterdnd2>=0.3.0
```

### Windows Defender блокирует `.exe`
**Решение:** Нажмите «Подробнее» → «Выполнить в любом случае» в диалоге предупреждения.

---

## Примеры использования

### Пример 1: Добавить collaborator'ов в приватный репо

1. Создай файл `users.txt`:
```
alice
bob
charlie
```

2. Запусти GUI версию
3. Выбери файл через drag-n-drop
4. Введи репо: `myorg/private-repo`
5. Нажми «Выполнить»

### Пример 2: Удалить collaborator'ов из публичного репо

1. Переключись на режим **Delete**
2. Выбери репозиторий из истории (выпадающий список)
3. Загрузи файл с никами
4. Нажми «Выполнить»

---

## План развития

- [ ] Шифрование токена в USERDATA.json
- [ ] Просмотр текущих collaborator'ов репозитория
- [ ] Синхронизация (добавить новых, удалить старых, обновить уровни)
- [ ] Работа с несколькими репозиториями одновременно
- [ ] Web-версия приложения
- [ ] VS Code extension
- [ ] Экспорт результатов в CSV/JSON

---

*Proudly made by Popov Dmitrii*

---
---

# GitHub Collaborator Adder {#github-collaborator-adder-ro}

> 🇷🇺 [Versiunea în limba rusă](#github-collaborator-adder)

Un instrument pentru adăugarea în masă a utilizatorilor GitHub într-un depozit ca colaboratori. Disponibil în două versiuni: script în linie de comandă și interfață grafică cu suport pentru teme deschise/întunecate.

**Versiune:** 1.0 | **Licență:** MIT | **Autor:** Popov Dmitrii

---

## 📚 Documentație

- **[CHANGELOG.md](CHANGELOG.md)** — lista completă a modificărilor și noilor funcții
- **[RELEASE_NOTES.md](RELEASE_NOTES.md)** — notă scurtă la lansare

---

## Lansarea versiunii compilate pe Windows

Dacă nu doriți să instalați Python, puteți utiliza fișierul executabil `.exe` gata pregătit, care este deja inclus în depozit.

Descărcați fișierul `add_collaborators_gui.exe` de pe pagina de lansare: [**versiunea 0.5**](https://github.com/OWNER/REPO/releases/tag/v1.0)

După descărcare, plasați `add_collaborators_gui.exe` într-un dosar convenabil. La prima lansare, alături va fi creat automat fișierul `USERDATA.json` pentru stocarea datelor dumneavoastră. Nu este necesară nicio instalare — este suficient să faceți dublu clic pe fișier.

> **Atenție:** Windows Defender sau un alt antivirus poate afișa un avertisment la prima lansare — acesta este comportamentul standard pentru fișierele `.exe` nesemnate. Apăsați «Mai multe informații» → «Rulați oricum» pentru a continua.

---

## Fișierele proiectului

| Fișier | Descriere |
|---|---|
| `add_collaborators_gui.py` | Versiunea GUI — interfață grafică (tkinter) |
| `add_collaborators.py` | Versiunea CLI — întrebări interactive în terminal |
| `add_collaborators_gui.exe` | Versiunea compilată pentru Windows |
| `USERDATA.json` | Creat automat — stochează utilizatorul, tokenul și istoricul repo |
| `requirements.txt` | Lista dependențelor |
| `README.md` | Acest fișier (documentație) |
| `CHANGELOG.md` | Toate modificările și îmbunătățirile |
| `RELEASE_NOTES.md` | Notă scurtă la lansare |

---

## Cerințe (pentru rularea din codul sursă)

Python 3.8+ și două biblioteci externe:

```bash
pip install -r requirements.txt
```

Sau manual:

```bash
pip install certifi tkinterdnd2
```

Tot restul face parte din biblioteca standard Python.

---

## Formatul fișierului de intrare

Un fișier `.txt` simplu, cu un username GitHub pe fiecare linie:

```
octocat
torvalds
# liniile care încep cu # sunt ignorate
someuser
```

---

## Versiunea CLI — `add_collaborators.py`

<details>
<summary>Afișați instrucțiunile</summary>

Pornire:

```bash
python add_collaborators.py
```

Scriptul pune întrebări pe rând:

1. Calea către fișierul `.txt` cu username-uri
2. Depozitul în formatul `OWNER/REPO`
3. Username-ul dumneavoastră GitHub
4. Tokenul dumneavoastră GitHub
5. Nivelul de acces (`pull` / `push` / `maintain` / `triage` / `admin`)

Dacă username-ul sau tokenul diferă față de cele salvate — veți fi întrebat dacă doriți să actualizați `USERDATA.json`.

</details>

---

## Versiunea GUI — `add_collaborators_gui.py`

<details>
<summary>Afișați instrucțiunile</summary>

Pornire:

```bash
python add_collaborators_gui.py
```

### Caracteristici principale

**Interfață:**
- Temă întunecată și deschisă (butonul ☀️/🌙) — fundal `#0E0E0B`/`#F5F5F5`, accente `#AFE607`/`#8BC034`
- Trei limbi: **RU** / **EN** / **RO** (comutare instantanee)
- Design profesional cu paletă contrastantă

**Lucru cu fișiere și repo:**
- Drag-n-drop fișiere — trage fișierul `.txt` direct în câmp, sau folosește butonul «Răsfoire»
- Istoricul depozitelor — listă derulantă cu ultimele 10 depozite utilizate
- Username-ul și tokenul sunt încărcate automat din `USERDATA.json` la pornire
- Câmpul depozitului este pre-completat cu `username/` — este necesar doar să scrieți numele depozitului după slash
- La modificarea username-ului, prefixul din câmpul depozitului se actualizează automat

**Operații:**
- Verificarea tokenului — butonul «Verifica» lângă câmpul tokenului (validare rapidă via GitHub API)
- Două moduri de lucru:
  - **Add** — adaugă utilizatori cu nivelul de acces selectat (implicit)
  - **Delete** — elimină utilizatori din depozit (câmpul permisiune este ascuns)
- Selectarea nivelului de acces prin butoane radio (doar pentru modul Add)

**Monitorizare:**
- Jurnal cu ieșire colorată în timp real (verde — succes, roșu — eroare, galben — informații)
- Bară de progres care urmărește evoluția operației
- Status detaliat pentru fiecare utilizator (numar operație, rezultat)

**Salvare date:**
- Casetă de bifat pentru salvarea username-ului și tokenului în `USERDATA.json`
- Istoricul depozitelor se salvează automat la finalizarea cu succes
- Sincronizarea datelor se efectuează instantaneu

</details>

---

## Cum să obțineți un token GitHub

1. Accesați **GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)**
2. Apăsați **Generate new token**
3. Indicați scope-ul: `repo` (depozite private) sau `public_repo` (doar publice)
4. Copiați tokenul — acesta este afișat o singură dată

Link direct: https://github.com/settings/tokens/new

---

## Niveluri de acces

| Nivel | Descriere |
|---|---|
| `pull` | Doar citire |
| `push` | Citire și scriere (implicit) |
| `maintain` | Gestionarea depozitului fără acces la setări |
| `triage` | Gestionarea issues și pull request-urilor |
| `admin` | Acces complet inclusiv setări |

---

## USERDATA.json

Salvat automat la confirmare. Se află în același dosar cu scriptul sau fișierul `.exe`.

```json
{
  "github_username": "username_dvs",
  "github_token": "ghp_xxxxxxxxxxxx",
  "repo_history": ["owner1/repo1", "owner2/repo2"]
}
```

> **Păstrați acest fișier în siguranță** — conține tokenul dumneavoastră GitHub.

---

## Note

- Între apelurile API se menține o pauză de 300 ms — pentru a nu depăși limita de rată GitHub
- Utilizatorii care sunt deja colaboratori vor primi nivelul de acces actualizat fără erori (status `204`)
- Utilizatorii noi vor primi o invitație care trebuie acceptată (status `201`)
- Eroarea `401` înseamnă că tokenul este invalid sau expirat — generați unul nou
- Istoricul repo se stochează local și este limitat la 10 depozite recente

---

## Probleme cunoscute și soluții

### Eroare SSL la pornire
**Soluție:** Instalați certifi:
```bash
pip install certifi
```

### Tkinterdnd2 nu este instalat
**Soluție:** Utilizați butonul Răsforie în loc de drag-n-drop sau instalați:
```bash
pip install tkinterdnd2>=0.3.0
```

### Windows Defender blochează fișierul `.exe`
**Soluție:** Apăsați «Mai multe informații» → «Rulați oricum» în dialogul de avertisment.

---

## Exemple de utilizare

### Exemplul 1: Adăugare colaboratori într-un depozit privat

1. Creează fișierul `users.txt`:
```
alice
bob
charlie
```

2. Lansează versiunea GUI
3. Selectează fișierul prin drag-n-drop
4. Introdu depozitul: `myorg/private-repo`
5. Apasă «Executa»

### Exemplul 2: Eliminare colaboratori din depozit public

1. Comută modul la **Delete**
2. Selectează depozitul din istoric (listă derulantă)
3. Încarcă fișierul cu utilizatori
4. Apasă «Executa»

---

## Planul de dezvoltare

- [ ] Criptarea tokenului în USERDATA.json
- [ ] Vizualizare colaboratori actuali ai depozitului
- [ ] Sincronizare (adaugă noi, elimină vechi, actualizează niveluri)
- [ ] Lucru cu mai multe depozite simultan
- [ ] Versiune web a aplicației
- [ ] Extensie VS Code
- [ ] Export rezultate în CSV/JSON

---

*Proudly made by Popov Dmitrii*
