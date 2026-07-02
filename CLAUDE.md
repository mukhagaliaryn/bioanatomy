# Bioanatomy — Техникалық анықтама

## Жылдам бастау

```bash
# Виртуалды ортаны іске қосу
source env/bin/activate

# Django сервері
python manage.py runserver

# Tailwind CSS (dev режим, watch)
cd ui/static_src && npm run dev

# Tailwind CSS (production build)
cd ui/static_src && npm run build

# Миграция жасау
python manage.py makemigrations
python manage.py migrate
```

## Модель иерархиясы

```
Subject (Пән)
  └── Chapter (Бөлім)
        └── Lesson (Модуль) ← verbose_name='Модуль', class аты Lesson болып қалады
              └── Task (Тапсырма)
                    ├── Theory
                    ├── Video
                    ├── Question → Option
                    └── Simulator

UserSubject → UserChapter → UserLesson → UserTask
                                └── UserTheory / UserVideo / UserAnswer / UserSimulator
```

## Маңызды конвенция

`Lesson` моделінің класс аты өзгертілмеген, бірақ `verbose_name='Модуль'`. Шаблондар мен UI-де "Сабақ" емес, "Модуль" деп аталады. Код ішінде (Python) `Lesson`, `user_lesson`, `lesson_id` деген айнымалы атаулар сақталған.

## URL схемасы

```
/                                          → кіру беті (login)
/account/login/                            → login
/account/register/                         → register
/account/user/me/                          → профиль
/student/                                  → студент панелі
/student/subject/<pk>/                     → пән беті
/student/user/subject/<s>/chapter/<c>/lesson/<l>/        → модуль беті
/student/user/subject/<s>/chapter/<c>/lesson/<l>/task/<t>/ → тапсырма беті
/teacher/                                  → мұғалім панелі
/admin/                                    → Django admin
```

## Frontend

- **Tailwind CSS v4** — `@theme` директивасы арқылы конфигурацияланады (`ui/static_src/src/styles.css`)
- **Негізгі түс**: `--color-primary-*` → orange (orange-50 … orange-950)
- **DaisyUI v5** + **Flowbite v3** — компонент кітапханалары
- **Жинау**: `cd ui/static_src && npm run build` → `ui/static/css/dist/styles.css`
- **PostCSS** плагиндері: `@tailwindcss/postcss`, `postcss-simple-vars`, `postcss-nested`

## Шаблон иерархиясы

```
base.html
  └── layouts/base_layout.html      (navbar)
        ├── layouts/lesson_layout.html   (бүйір панель — модуль тізімі)
        │     └── app/dashboard/student/user/.../lesson/page.html
        └── layouts/task_layout.html     (жоғарғы навигация — тапсырмалар)
              └── app/dashboard/student/user/.../task/page.html
                    └── components/app/task_*.html (theory/video/test/simulator)
```

## Орта айнымалылары (.env)

```
SECRET_KEY=...
DEBUG=True
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=localhost
DB_PORT=5432
```

## Пайдаланушы типтері

- `student` — студент (default)
- `teacher` — мұғалім
- `admin` — әкімші

`LOGIN_REDIRECT_URL = 'student'` — кіргеннен кейін студент панеліне бағыттайды. Мұғалімдер `/teacher/` мекенжайына қолмен өтеді.

## Миграция тарихи (core)

| # | Не жасайды |
|---|------------|
| 0001 | Барлық негізгі модельдерді жасайды |
| 0002–0004 | owner, cert, view, lab_link өрістерін жояды |
| 0005 | written/matching тапсырма типтерін жояды |
| 0006 | Simulator, Theory, UserSimulator, UserTheory қосады |
| 0007–0009 | Кішігірім өріс тазалаулары |
| 0010 | Lesson → Модуль verbose_name өзгерісі |
