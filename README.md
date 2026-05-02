# GitHub Collaborator Adder

> 🇷🇴 [Versiunea în limba română](#github-collaborator-adder-ro)

Инструмент для массового добавления пользователей GitHub в репозиторий в роли collaborator. Доступен в двух версиях: консольный скрипт и графический интерфейс.

---

## Запуск скомпилированной версии под Windows

Если вы не хотите устанавливать Python, воспользуйтесь готовым исполняемым файлом `.exe`, который уже включён в репозиторий.

Загрузите файл `add_collaborators_gui.exe` со страницы релиза: [**версия 0.5**](https://github.com/dimon453/GithubManager/releases/tag/v.05)

После загрузки поместите `add_collaborators_gui.exe` в удобную папку. При первом запуске рядом автоматически создастся файл `USERDATA.json` для хранения ваших данных. Никакая установка не требуется — достаточно дважды щёлкнуть по файлу.

> **Обратите внимание:** Windows Defender или другой антивирус может показать предупреждение при первом запуске — это стандартное поведение для неподписанных `.exe` файлов. Нажмите «Подробнее» → «Выполнить в любом случае» для продолжения.

---

## Файлы проекта

| Файл | Описание |
|---|---|
| `add_collaborators.py` | CLI версия — интерактивные вопросы в терминале |
| `add_collaborators_gui.py` | GUI версия — графический интерфейс (tkinter) |
| `add_collaborators_gui.exe` | Скомпилированная версия для Windows |
| `USERDATA.json` | Создаётся автоматически — хранит username и токен |

---

## Требования (для запуска из исходного кода)

Python 3.8+ и одна внешняя библиотека:

```bash
pip install certifi
```

Всё остальное входит в стандартную библиотеку Python — ничего дополнительно устанавливать не нужно.

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

Возможности:
- Тёмная тема (фон `#0E0E0B`, акценты `#AFE607`)
- Username и токен загружаются автоматически из `USERDATA.json` при старте
- Поле репозитория заполняется как `username/` — необходимо только дописать название репо
- При изменении username префикс в поле репозитория обновляется автоматически
- Диалог выбора файла (кнопка «Обзор»)
- Выбор уровня доступа через радиокнопки
- Лог с цветным выводом в реальном времени (зелёный — успех, красный — ошибка)
- Прогресс-бар
- Чекбокс для сохранения данных в `USERDATA.json`
- Переключатель языка: **RU / EN / RO**

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
  "github_token": "ghp_xxxxxxxxxxxx"
}
```

> **Храните этот файл в безопасном месте** — он содержит ваш GitHub токен.

---

## Примечания

- Между API-запросами выдерживается пауза 300 мс — чтобы не превышать rate limit GitHub
- Пользователи, которые уже являются collaborator'ами, получат обновлённый уровень доступа без ошибок (статус `204`)
- Новые пользователи получат приглашение, которое необходимо принять (статус `201`)
- Ошибка `401` означает, что токен недействителен или истёк — сгенерируйте новый

---

*Proudly made by Popov Dmitrii*

---
---

# GitHub Collaborator Adder {#github-collaborator-adder-ro}

> 🇷🇺 [Версия на русском языке](#github-collaborator-adder)

Un instrument pentru adăugarea în masă a utilizatorilor GitHub într-un depozit ca colaboratori. Disponibil în două versiuni: script în linie de comandă și interfață grafică.

---

## Lansarea versiunii compilate pe Windows

Dacă nu doriți să instalați Python, puteți utiliza fișierul executabil `.exe` gata pregătit, care este deja inclus în depozit.

Descărcați fișierul `add_collaborators_gui.exe` de pe pagina de lansare: [**versiunea 0.5**](https://github.com/dimon453/GithubManager/releases/tag/v.05)

După descărcare, plasați `add_collaborators_gui.exe` într-un dosar convenabil. La prima lansare, alături va fi creat automat fișierul `USERDATA.json` pentru stocarea datelor dumneavoastră. Nu este necesară nicio instalare — este suficient să faceți dublu clic pe fișier.

> **Atenție:** Windows Defender sau un alt antivirus poate afișa un avertisment la prima lansare — acesta este comportamentul standard pentru fișierele `.exe` nesemnate. Apăsați «Mai multe informații» → «Rulați oricum» pentru a continua.

---

## Fișierele proiectului

| Fișier | Descriere |
|---|---|
| `add_collaborators.py` | Versiunea CLI — întrebări interactive în terminal |
| `add_collaborators_gui.py` | Versiunea GUI — interfață grafică (tkinter) |
| `add_collaborators_gui.exe` | Versiunea compilată pentru Windows |
| `USERDATA.json` | Creat automat — stochează username-ul și tokenul |

---

## Cerințe (pentru rularea din codul sursă)

Python 3.8+ și o singură bibliotecă externă:

```bash
pip install certifi
```

Tot restul face parte din biblioteca standard Python — nu este necesar să instalați nimic suplimentar.

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

Funcționalități:
- Temă întunecată (fundal `#0E0E0B`, accente `#AFE607`)
- Username-ul și tokenul sunt încărcate automat din `USERDATA.json` la pornire
- Câmpul depozitului este pre-completat cu `username/` — este necesar doar să scrieți numele depozitului după slash
- La modificarea username-ului, prefixul din câmpul depozitului se actualizează automat
- Dialog de selectare a fișierului (butonul «Răsfoire»)
- Selectarea nivelului de acces prin butoane radio
- Jurnal cu ieșire colorată în timp real (verde — succes, roșu — eroare)
- Bară de progres
- Casetă de bifat pentru salvarea datelor în `USERDATA.json`
- Comutator de limbă: **RU / EN / RO**

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
  "github_token": "ghp_xxxxxxxxxxxx"
}
```

> **Păstrați acest fișier în siguranță** — conține tokenul dumneavoastră GitHub.

---

## Note

- Între apelurile API se menține o pauză de 300 ms — pentru a nu depăși limita de rată GitHub
- Utilizatorii care sunt deja colaboratori vor primi nivelul de acces actualizat fără erori (status `204`)
- Utilizatorii noi vor primi o invitație care trebuie acceptată (status `201`)
- Eroarea `401` înseamnă că tokenul este invalid sau expirat — generați unul nou

---

*Proudly made by Popov Dmitrii*