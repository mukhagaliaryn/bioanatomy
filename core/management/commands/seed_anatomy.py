from django.core.management.base import BaseCommand
from core.models.subjects import Subject, Lesson
from core.models.tasks import Task, Theory, Video, Question, Option, MatchingPair


SUBJECT_DATA = {
    'name': 'Адам анатомиясы',
    'author': 'Биология мұғалімі',
    'description': (
        '<p>«Адам анатомиясы» — адам ағзасының құрылысын, мүшелер жүйелерінің қызметін '
        'және олардың өзара байланысын зерттейтін кешенді оқу курсы.</p>'
        '<p>Бұл курс мұғалімдерге цифрлық технологиялар мен креативті педагогикалық '
        'тәсілдерді ұштастыра отырып, анатомияны тереңірек меңгеруге және оқушыларға '
        'тиімді жеткізуге мүмкіндік береді.</p>'
    ),
}

# Тапсырма түрлері: theory, video, test, matching
# Комбинациялар:
#   1 — Теория + Тест + Сәйкестендіру   (20 + 50 + 30 = 100)
#   2 — Видео + Тест + Сәйкестендіру    (10 + 60 + 30 = 100)
#   3 — Видео + Тест                    (30 + 70 = 100)
#   4 — Тек Видео                       (100)
#   5 — Тек Тест                        (100)
#   6 — Теория + Видео + Тест + Сәйкест (15 + 15 + 40 + 30 = 100)

LESSONS_DATA = [
    # ── 1. Теория + Тест + Сәйкестендіру ─────────────────────────────────────
    {
        'title': 'Креативті педагогика',
        'description': 'Мұғалімдердің креативті қабілеттерін дамытуға арналған теориялық бөлім.',
        'order': 1,
        'tasks': [
            {
                'type': 'theory',
                'rating': 20,
                'duration': 10,
                'order': 1,
                'theories': [
                    {
                        'content': (
                            '<h3>Креативті педагогика дегеніміз не?</h3>'
                            '<p>Креативті педагогика — оқушылардың шығармашылық ойлауын, '
                            'қиялын және проблеманы шешу қабілетін дамытуға бағытталған '
                            'педагогикалық тәсіл. Бұл тәсіл дәстүрлі оқытудан ерекшеленіп, '
                            'оқушыны оқу процесінің белсенді қатысушысына айналдырады.</p>'
                            '<h3>Блум таксономиясы</h3>'
                            '<p>Блум таксономиясы — оқу мақсаттарын алты деңгейге бөлетін модель: '
                            'білу, түсіну, қолдану, талдау, бағалау, жасау. '
                            'Жоғары деңгейлер (бағалау, жасау) — креативтіліктің белгісі.</p>'
                        ),
                        'order': 1,
                    },
                ],
            },
            {
                'type': 'test',
                'rating': 50,
                'duration': 15,
                'order': 2,
                'questions': [
                    {
                        'text': 'Блум таксономиясында ең жоғары ойлау деңгейі қайсысы?',
                        'question_type': 'simple',
                        'order': 1,
                        'options': [
                            ('Білу', False, 0),
                            ('Түсіну', False, 0),
                            ('Талдау', False, 0),
                            ('Жасау (Синтез)', True, 10),
                        ],
                    },
                    {
                        'text': 'Рефлексия білім беруде не үшін қолданылады?',
                        'question_type': 'simple',
                        'order': 2,
                        'options': [
                            ('Сабақты тезірек аяқтау үшін', False, 0),
                            ('Оқушыларды жазалау үшін', False, 0),
                            ('Өзін-өзі бағалауға және ойлануға үйрету үшін', True, 10),
                            ('Үй тапсырмасын берместен бұрын', False, 0),
                        ],
                    },
                    {
                        'text': 'Креативті педагогиканың негізгі мақсаты қандай?',
                        'question_type': 'simple',
                        'order': 3,
                        'options': [
                            ('Оқушылардың шығармашылық қабілеттерін дамыту', True, 10),
                            ('Тек академиялық білімді жеткізу', False, 0),
                            ('Тәртіпті қатаң сақтату', False, 0),
                            ('Оқулықты толық жаттату', False, 0),
                        ],
                    },
                    {
                        'text': 'Мұғалімнің креативтілігі оқу процесіне қалай оң әсер етеді?',
                        'question_type': 'multiple',
                        'order': 4,
                        'options': [
                            ('Оқушылардың қызығушылығын арттырады', True, 5),
                            ('Сабақты қызықты етеді', True, 5),
                            ('Үлгерімді төмендетеді', False, 0),
                            ('Жаңа идеяларды туғызады', True, 5),
                        ],
                    },
                ],
            },
            {
                'type': 'matching',
                'rating': 30,
                'duration': 10,
                'order': 3,
                'pairs': [
                    ('Блум таксономиясы', 'Ойлау деңгейлерін сипаттайтын педагогикалық модель', 1),
                    ('Рефлексия', 'Оқушының өз ойын саралауы және бағалауы', 2),
                    ('Дивергентті ойлау', 'Бір мәселеге бірнеше шешім іздеу', 3),
                    ('Конвергентті ойлау', 'Бір дұрыс жауапқа бағытталған ойлау', 4),
                ],
            },
        ],
    },

    # ── 2. Видео + Тест + Сәйкестендіру ──────────────────────────────────────
    {
        'title': '«Адам анатомиясы» цифрлық курсы',
        'description': 'Интер��ктивті 3D модельдер, AR бейнелер, анатомиялық жүйелердің құрылымы.',
        'order': 2,
        'tasks': [
            {
                'type': 'video',
                'rating': 10,
                'duration': 10,
                'order': 1,
                'url': 'https://www.youtube.com/embed/Ae4MadKPJhg',
            },
            {
                'type': 'test',
                'rating': 60,
                'duration': 15,
                'order': 2,
                'questions': [
                    {
                        'text': 'Адам ағзасындағы ең үлкен орган қайсысы?',
                        'question_type': 'simple',
                        'order': 1,
                        'options': [
                            ('Бауыр', False, 0),
                            ('Жүрек', False, 0),
                            ('Тері', True, 10),
                            ('Өкпе', False, 0),
                        ],
                    },
                    {
                        'text': 'Адамның жүрегі қалыпты жағдайда бір минутта қанша рет соғады?',
                        'question_type': 'simple',
                        'order': 2,
                        'options': [
                            ('30–40 рет', False, 0),
                            ('60–100 рет', True, 10),
                            ('120–140 рет', False, 0),
                            ('150–200 рет', False, 0),
                        ],
                    },
                    {
                        'text': 'Қандай мүше қанды сүзіп тазартуға жауапты?',
                        'question_type': 'simple',
                        'order': 3,
                        'options': [
                            ('Жүрек', False, 0),
                            ('Өкпе', False, 0),
                            ('Бүйрек', True, 10),
                            ('Бауыр', False, 0),
                        ],
                    },
                    {
                        'text': 'Адам ағзасындағы сүйектерге қатысты дұрыс тұжырымдарды таңдаңыз:',
                        'question_type': 'multiple',
                        'order': 4,
                        'options': [
                            ('Жаңа туған нәрестеде шамамен 270 сүйек болады', True, 5),
                            ('Ересек адамда 206 сүйек болады', True, 5),
                            ('Барлық адамда сүйек саны дәл бірдей', False, 0),
                            ('Бас сүйегі 22 бөліктен тұрады', True, 5),
                        ],
                    },
                ],
            },
            {
                'type': 'matching',
                'rating': 30,
                'duration': 10,
                'order': 3,
                'pairs': [
                    ('Жүрек', 'Қанды айдайтын бұлшықетті орган', 1),
                    ('Өкпе', 'Газ алмасуды қамтамасыз ететін орган', 2),
                    ('Бауыр', 'Қанды тазартатын және өт бөлетін орган', 3),
                    ('Бүйрек', 'Несеп шығару жүйесінің негізгі органы', 4),
                    ('Ми', 'Орталық жүйке жүйесінің басты органы', 5),
                ],
            },
        ],
    },

    # ── 3. Видео + Тест ───────────────────────────────────────────────────────
    {
        'title': 'Креативті тапсырмалар банкі',
        'description': 'Ойын, жоба, mind-map, storytelling секілді тапсырмалар шаблондары.',
        'order': 3,
        'tasks': [
            {
                'type': 'video',
                'rating': 30,
                'duration': 15,
                'order': 1,
                'url': 'https://www.youtube.com/embed/5zIR6DRxFQo',
            },
            {
                'type': 'test',
                'rating': 70,
                'duration': 20,
                'order': 2,
                'questions': [
                    {
                        'text': 'Mind-map (ойлар картасы) не үшін пайдаланылады?',
                        'question_type': 'simple',
                        'order': 1,
                        'options': [
                            ('Математикалық есептерді шешу үшін', False, 0),
                            ('Идеяларды визуалды түрде ұйымдастыру үшін', True, 10),
                            ('Тест тапсыру үшін', False, 0),
                            ('Үй тапсырмасын орындау үшін', False, 0),
                        ],
                    },
                    {
                        'text': 'Storytelling әдісі білім беруде қандай мақсатта қолданылады?',
                        'question_type': 'simple',
                        'order': 2,
                        'options': [
                            ('Тек мектепке дейінгі балалар үшін', False, 0),
                            ('Оқушылардың қиялы мен байланыс орнату қабілетін дамыту үшін', True, 10),
                            ('Тапсырма санын азайту үшін', False, 0),
                            ('Сынып тәртібін сақтау үшін', False, 0),
                        ],
                    },
                    {
                        'text': 'Жоба әдісінің (project-based learning) негізгі белгілерін таңдаңыз:',
                        'question_type': 'multiple',
                        'order': 3,
                        'options': [
                            ('Оқушы нақты мәселені шешеді', True, 5),
                            ('Командамен жұмыс жасалады', True, 5),
                            ('Тек оқулықтан оқу арқылы орындалады', False, 0),
                            ('Нәтиже нақты пайдаланушы үшін маңызды болады', True, 5),
                        ],
                    },
                ],
            },
        ],
    },

    # ── 4. Тек Видео ──────────────────────────────────────────────────────────
    {
        'title': 'Цифрлық құралдар шеберханасы',
        'description': 'Canva, Genially, BioDigital Human, Kahoot, Quizizz — бейне-нұсқаулықтар.',
        'order': 4,
        'tasks': [
            {
                'type': 'video',
                'rating': 100,
                'duration': 30,
                'order': 1,
                'url': 'https://www.youtube.com/embed/nLGV8XnJIoE',
            },
        ],
    },

    # ── 5. Тек Тест ───────────────────────────────────────────────────────────
    {
        'title': 'Бағалау және кері байланыс',
        'description': 'Креативтілік индексін бағалау рубрикалары, өзіндік талдау парақтары.',
        'order': 5,
        'tasks': [
            {
                'type': 'test',
                'rating': 100,
                'duration': 20,
                'order': 1,
                'questions': [
                    {
                        'text': 'Рубрика бағалауда не үшін қолданылады?',
                        'question_type': 'simple',
                        'order': 1,
                        'options': [
                            ('Тек мұғалімге жасырын баллдар қоюға', False, 0),
                            ('Бағалау критерийлерін алдын ала анық белгілеу үшін', True, 10),
                            ('Оқушыларды жазалау үшін', False, 0),
                            ('Тек жазбаша жұмыстарды тексеру үшін', False, 0),
                        ],
                    },
                    {
                        'text': 'Формативті бағалау қашан жүргізіледі?',
                        'question_type': 'simple',
                        'order': 2,
                        'options': [
                            ('Тек оқу жылының соңында', False, 0),
                            ('О��у барысында үздіксіз, кері байланыс беру мақсатында', True, 10),
                            ('Тоқсанда тек бір рет', False, 0),
                            ('Емтихан кезінде ғана', False, 0),
                        ],
                    },
                    {
                        'text': 'Өзіндік бағалаудың (self-assessment) оқу процесіндегі рөлі қандай?',
                        'question_type': 'multiple',
                        'order': 3,
                        'options': [
                            ('Оқушы өз жетістіктерін саралайды', True, 5),
                            ('Метакогниция және ойлау дағдылары дамиды', True, 5),
                            ('Мұғалімнің жұмысын толығымен азайтады', False, 0),
                            ('Оқушының жауапкершілік сезімі артады', True, 5),
                        ],
                    },
                    {
                        'text': 'Суммативті бағалау қандай мақсатта жүргізіледі?',
                        'question_type': 'simple',
                        'order': 4,
                        'options': [
                            ('Оқу барысында кері байланыс беру', False, 0),
                            ('Оқу кезеңінің соңында жалпы нәтижені анықтау', True, 10),
                            ('Тек жазбаша жұмыс тексеру', False, 0),
                            ('Оқушыны мотивациялау', False, 0),
                        ],
                    },
                ],
            },
        ],
    },

    # ── 6. Теория + Видео + Тест + Сәйкестендіру (барлық түр) ───────────────
    {
        'title': 'Портфолио',
        'description': 'Мұғалімнің жетістіктері, жобалары мен сертификаттары сақталатын бөлім.',
        'order': 6,
        'tasks': [
            {
                'type': 'theory',
                'rating': 15,
                'duration': 10,
                'order': 1,
                'theories': [
                    {
                        'content': (
                            '<h3>Педагогикалық портфолио</h3>'
                            '<p>Портфолио — мұғалімнің кәсіби өсуін, жетістіктерін және '
                            'тәжірибесін жүйелі түрде құжаттайтын жинақ. '
                            'Ол мұғалімге өзінің даму жолын бақылауға, '
                            'рефлексия жасауға және кәсіби мақсаттарды айқындауға көмектеседі.</p>'
                            '<h3>e-Portfolio артықшылықтары</h3>'
                            '<p>Цифрлық портфолио жұмыстарды кез-келген жерден қарауға, '
                            'бөлісуге және жаңартуға мүмкіндік береді. '
                            'Google Sites, Mahara, Notion сияқты платформаларда жасалады.</p>'
                        ),
                        'order': 1,
                    },
                ],
            },
            {
                'type': 'video',
                'rating': 15,
                'duration': 10,
                'order': 2,
                'url': 'https://www.youtube.com/embed/XZ0SjFJlxb0',
            },
            {
                'type': 'test',
                'rating': 40,
                'duration': 15,
                'order': 3,
                'questions': [
                    {
                        'text': 'Педагогикалық портфолионың негізгі мақсаты қандай?',
                        'question_type': 'simple',
                        'order': 1,
                        'options': [
                            ('Мұғалімнің жалақысын автоматты арттыру', False, 0),
                            ('Мұғалімнің кәсіби өсуін және жетістіктерін жүйелі сақтау', True, 10),
                            ('Тек тексеру органдары үшін дайындалады', False, 0),
                            ('Тек жаңа мұғалімдерге арналған', False, 0),
                        ],
                    },
                    {
                        'text': 'e-Portfolio не береді?',
                        'question_type': 'simple',
                        'order': 2,
                        'options': [
                            ('Тек қағаз форматта сақтауға мүмкіндік береді', False, 0),
                            ('Жұмыстарды цифрлық ортада жинақтауға және бөлісуге мүмкіндік береді', True, 10),
                            ('Тек суреттер қоюға болады', False, 0),
                            ('Ешкімге қол жетімді болмайды', False, 0),
                        ],
                    },
                    {
                        'text': 'Портфолиоға кіретін мазмұнды таңд��ңыз:',
                        'question_type': 'multiple',
                        'order': 3,
                        'options': [
                            ('Кәсіби жетістіктер сертификаттары', True, 5),
                            ('Сабақ жоспарлары мен оқу материалдары', True, 5),
                            ('Өзіндік рефлексия жазбалары', True, 5),
                            ('Оқушылардың жеке деректері (дербес ақпарат)', False, 0),
                        ],
                    },
                ],
            },
            {
                'type': 'matching',
                'rating': 30,
                'duration': 10,
                'order': 4,
                'pairs': [
                    ('e-Portfolio', 'Жетістіктерді цифрлық форматта сақтайтын онлайн кеңістік', 1),
                    ('Артефакт', 'Портфолиодағы нақты жұмыс үлгісі немесе жетістік дәлелі', 2),
                    ('Рефлексия жазбасы', 'Тәжірибеден алған сабақты талдайтын жеке жазба', 3),
                    ('Сертификат', 'Кәсіби даму немесе оқуды растайтын ресми құжат', 4),
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = 'Адам анатомиясы пәні үшін тест деректерін базаға салады'

    def handle(self, *args, **options):
        self.stdout.write('Деректерді базаға салу басталды...\n')

        subject, created = Subject.objects.get_or_create(
            name=SUBJECT_DATA['name'],
            defaults={
                'description': SUBJECT_DATA['description'],
                'author': SUBJECT_DATA['author'],
            },
        )
        if not created and not subject.author:
            subject.author = SUBJECT_DATA['author']
            subject.save(update_fields=['author'])
        self.stdout.write(f'  Пән: {subject.name} [{"Жасалды" if created else "Бұрыннан бар"}]')

        for lesson_data in LESSONS_DATA:
            lesson, created = Lesson.objects.get_or_create(
                subject=subject,
                order=lesson_data['order'],
                defaults={
                    'title': lesson_data['title'],
                    'description': lesson_data['description'],
                },
            )
            types = ', '.join(t['type'] for t in lesson_data['tasks'])
            total = sum(t['rating'] for t in lesson_data['tasks'])
            self.stdout.write(
                f'\n  {lesson_data["order"]}-модуль: {lesson.title} '
                f'[{"Жасалды" if created else "Бұрыннан бар"}]'
                f'\n    Тапсырмалар: {types} | Жиыны: {total} балл'
            )

            if created:
                for task_data in lesson_data['tasks']:
                    self._create_task(lesson, task_data)

        self.stdout.write(self.style.SUCCESS('\nДеректер сәтті базаға салынды!'))

    def _create_task(self, lesson, task_data):
        task_type = task_data['type']
        task = Task.objects.create(
            lesson=lesson,
            task_type=task_type,
            rating=task_data['rating'],
            duration=task_data['duration'],
            order=task_data['order'],
        )

        if task_type == 'theory':
            for t in task_data['theories']:
                Theory.objects.create(task=task, content=t['content'], order=t['order'])
            self.stdout.write(f'    ✓ Теория ({task_data["rating"]} балл)')

        elif task_type == 'video':
            Video.objects.create(task=task, url=task_data['url'], order=1)
            self.stdout.write(f'    ✓ Видео ({task_data["rating"]} балл)')

        elif task_type == 'test':
            for q in task_data['questions']:
                question = Question.objects.create(
                    task=task,
                    text=q['text'],
                    question_type=q['question_type'],
                    order=q['order'],
                )
                for text, is_correct, score in q['options']:
                    Option.objects.create(
                        question=question, text=text,
                        is_correct=is_correct, score=score,
                    )
            self.stdout.write(
                f'    ✓ Тест ({len(task_data["questions"])} сұрақ, {task_data["rating"]} балл)'
            )

        elif task_type == 'matching':
            for left, right, order in task_data['pairs']:
                MatchingPair.objects.create(
                    task=task, left_text=left, right_text=right, order=order,
                )
            self.stdout.write(
                f'    ✓ Сәйкестендіру ({len(task_data["pairs"])} жұп, {task_data["rating"]} балл)'
            )
