<p align="center">
    <img 
        src="ui/static/images/logo.svg" 
        alt="Bioanatomy логотипі" width="140" 
    />
</p>
<h3 align="center">Bioanatomy</h3>
<p align="center">
    Анатомия пәнін онлайн оқытуға арналған білім беру платформасы
</p>

---

## Жоба туралы

**Bioanatomy** — студенттерге анатомия пәнін интерактивті түрде оқытуға арналған Django негізіндегі веб-платформа. Жүйе субъект (пән), бөлім (chapter) және модуль (module) деңгейлерінде оқу процесін ұйымдастырады. Теория, бейне, тест және симулятор тапсырмалары арқылы студент прогресі нақты уақытта бақыланады.

## Негізгі мүмкіндіктер

- **Пәндер мен модульдер** — Subject → Chapter → Lesson (Модуль) иерархиясы
- **Тапсырма түрлері** — Теория, Бейне, Тест, Симулятор
- **Студент прогресі** — UserSubject, UserChapter, UserLesson, UserTask моделдері арқылы толық бақылау
- **Мұғалімдер панелі** — оқушылар статистикасын нақты уақытта қарау
- **Кері байланыс** — студент модульді аяқтағаннан кейін баға мен пікір қалдыра алады
- **Қазақ тілі** — интерфейс толығымен қазақ тілінде

## Технологиялар

| Категория | Технология |
|-----------|------------|
| Backend | Python 3.12, Django 5.x |
| Database | PostgreSQL (psycopg2-binary) |
| Frontend | Tailwind CSS v4, DaisyUI v5, Flowbite v3 |
| Rich text | CKEditor 4, Summernote |
| Auth | Django built-in (AbstractUser) |
| i18n | Қазақ (kk-kz), орыс, ағылшын |

## Орнату

```bash
# Виртуалды ортаны іске қосу
source env/bin/activate

# Тәуелділіктерді орнату
pip install -r requirements.txt

# .env файлын жасап, дерекқор параметрлерін толтыру
cp .env.example .env

# Миграцияларды қолдану
python manage.py migrate

# Frontend жинау
cd ui/static_src && npm install && npm run build && cd ../..

# Сервер іске қосу
python manage.py runserver
```

## Жоба құрылымы

```
bioanatomy/
├── apps/
│   ├── account/          # Тіркелу, кіру, профиль
│   ├── dashboard/
│   │   ├── student/      # Студент панелі
│   │   └── teacher/      # Мұғалім панелі
│   └── main/             # Кіру беті
├── config/               # Django конфигурациясы
├── core/                 # Негізгі модельдер мен логика
│   ├── models/
│   │   ├── subjects.py   # Subject, Chapter, Lesson (Модуль)
│   │   ├── tasks.py      # Task, Theory, Video, Question, Simulator
│   │   ├── user_subjects.py  # UserSubject, UserChapter, UserLesson
│   │   └── user_tasks.py    # UserTask, UserTheory, UserVideo
│   └── admin/            # Django admin конфигурациясы
└── ui/
    ├── static/           # Жиналған статикалық файлдар
    ├── static_src/       # Tailwind CSS көзі
    └── templates/        # HTML шаблондары
```
