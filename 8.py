Python
                         Копировать
                    import sqlite3
                    from contextlib import closing

                    # 1. Создание связанных таблиц
                    def create_related_tables():
                    """Создание связанных таблиц для демонстрации JOIN"""
                    with closing(sqlite3.connect("university_advanced.db")) as conn:
                    cursor = conn.cursor()

                    # Таблица факультетов
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS faculties (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    dean TEXT,
                    building TEXT
                    )
                    ''')

                    # Таблица студентов (с внешним ключом)
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    faculty_id INTEGER,
                    FOREIGN KEY (faculty_id) REFERENCES faculties(id)
                    )
                    ''')

                    # Таблица курсов
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    credits INTEGER,
                    faculty_id INTEGER,
                    FOREIGN KEY (faculty_id) REFERENCES faculties(id)
                    )
                    ''')

                    # Таблица оценок (многие-ко-многим)
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS grades (
                    student_id INTEGER,
                    course_id INTEGER,
                    grade INTEGER CHECK(grade >= 0 AND grade <= 100),
                    semester TEXT,
                    PRIMARY KEY (student_id, course_id, semester),
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                    )
                    ''')

                    conn.commit()
                    print("✅ Связанные таблицы созданы")

                    # 2. Добавление тестовых данных
                    def add_sample_data_advanced():
                    """Добавление тестовых данных в связанные таблицы"""
                    with closing(sqlite3.connect("university_advanced.db")) as conn:
                    cursor = conn.cursor()

                    # Добавляем факультеты
                    faculties = [
                    ("Информатика", "Иванов И.И.", "Корпус 1"),
                    ("Математика", "Петрова М.М.", "Корпус 2"),
                    ("Физика", "Сидоров А.А.", "Корпус 3")
                    ]

                    cursor.executemany(
                    "INSERT INTO faculties (name, dean, building) VALUES (?, ?, ?)",
                    faculties
                    )

                    # Добавляем студентов
                    students = [
                    ("Иван Иванов", 20, 1),
                    ("Мария Петрова", 21, 1),
                    ("Алексей Сидоров", 19, 2),
                    ("Елена Васильева", 22, 3),
                    ("Дмитрий Николаев", 20, 2)
                    ]

                    cursor.executemany(
                    "INSERT INTO students (name, age, faculty_id) VALUES (?, ?, ?)",
                    students
                    )

                    # Добавляем курсы
                    courses = [
                    ("Программирование", 4, 1),
                    ("Базы данных", 3, 1),
                    ("Математический анализ", 5, 2),
                    ("Линейная алгебра", 4, 2),
                    ("Общая физика", 4, 3),
                    ("Квантовая механика", 5, 3)
                    ]

                    cursor.executemany(
                    "INSERT INTO courses (name, credits, faculty_id) VALUES (?, ?, ?)",
                    courses
                    )

                    # Добавляем оценки
                    grades = [
                    (1, 1, 85, "2023-осень"),
                    (1, 2, 90, "2023-осень"),
                    (2, 1, 92, "2023-осень"),
                    (3, 3, 78, "2024-весна"),
                    (4, 5, 88, "2024-весна"),
                    (5, 4, 76, "2024-весна")
                    ]

                    cursor.executemany(
                    "INSERT INTO grades (student_id, course_id, grade, semester) VALUES (?, ?, ?, ?)",
                    grades
                    )

                    conn.commit()
                    print("✅ Тестовые данные добавлены")

                    # 3. INNER JOIN - студенты с факультетами
                    def inner_join_example():
                    """INNER JOIN: студенты с информацией о факультетах"""
                    with closing(sqlite3.connect("university_advanced.db")) as conn:
                    cursor = conn.cursor()

                    query = '''
                    SELECT
                    s.name AS student_name,
                    s.age,
                    f.name AS faculty_name,
                    f.dean,
                    f.building
                    FROM students s
                    INNER JOIN faculties f ON s.faculty_id = f.id
                    ORDER BY s.name
                    '''

                    cursor.execute(query)
                    return cursor.fetchall()

                    # 4. LEFT JOIN - все курсы, даже без оценок
                    def left_join_example():
                    """LEFT JOIN: все курсы и оценки по ним"""
                    with closing(sqlite3.connect("university_advanced.db")) as conn:
                    cursor = conn.cursor()

                    query = '''
                    SELECT
                    c.name AS course_name,
                    c.credits,
                    g.grade,
                    g.semester
                    FROM courses c
                    LEFT JOIN grades g ON c.id = g.course_id
                    ORDER BY c.name
                    '''

                    cursor.execute(query)
                    return cursor.fetchall()

                    # 5. Множественный JOIN
                    def multiple_join_example():
                    """JOIN трех таблиц: студенты, курсы, оценки"""
                    with closing(sqlite3.connect("university_advanced.db")) as conn:
                    cursor = conn.cursor()

                    query = '''
                    SELECT
                    s.name AS student_name,
                    c.name AS course_name,
                    g.grade,
                    g.semester,
                    f.name AS faculty_name
                    FROM grades g
                    JOIN students s ON g.student_id = s.id
                    JOIN courses c ON g.course_id = c.id
                    JOIN faculties f ON c.faculty_id = f.id
                    ORDER BY g.grade DESC
                    '''

                    cursor.execute(query)
                    return cursor.fetchall()

                    # 6. JOIN с агрегатными функциями
                    def join_with_aggregation():
                    """JOIN с группировкой и агрегатными функциями"""
                    with closing(sqlite3.connect("university_advanced.db")) as conn:
                    cursor = conn.cursor()

                    query = '''
                    SELECT
                    f.name AS faculty_name,
                    COUNT(s.id) AS student_count,
                    AVG(g.grade) AS avg_grade,
                    MAX(g.grade) AS max_grade,
                    MIN(g.grade) AS min_grade
                    FROM faculties f
                    LEFT JOIN students s ON f.id = s.faculty_id
                    LEFT JOIN grades g ON s.id = g.student_id
                    GROUP BY f.id
                    ORDER BY avg_grade DESC
                    '''

                    cursor.execute(query)
                    return cursor.fetchall()

                    # 7. Пример использования
                    if __name__ == "__main__":
                    print("=== JOIN ЗАПРОСЫ В SQLite ===")

                    # Создаем таблицы и данные
                    create_related_tables()
                    add_sample_data_advanced()

                    print("\n=== INNER JOIN: Студенты и факультеты ===")
                    students_with_faculties = inner_join_example()
                    for student in students_with_faculties:
                    print(f"Студент: {student[0]}, Возраст: {student[1]}, "
                    f"Факультет: {student[2]}, Декан: {student[3]}, Корпус: {student[4]}")

                    print("\n=== LEFT JOIN: Курсы и оценки ===")
                    courses_with_grades = left_join_example()
                    for course in courses_with_grades:
                    grade_display = f", Оценка: {course[2]}" if course[2] else ", Без оценок"
                    print(f"Курс: {course[0]}, Кредиты: {course[1]}{grade_display}, Семестр: {course[3] or 'Нет'}")

                    print("\n=== Множественный JOIN ===")
                    detailed_info = multiple_join_example()
                    for info in detailed_info:
                    print(f"Студент: {info[0]}, Курс: {info[1]}, Оценка: {info[2]}, "
                    f"Семестр: {info[3]}, Факультет: {info[4]}")

                    print("\n=== JOIN с агрегацией ===")
                    faculty_stats = join_with_aggregation()
                    for stats in faculty_stats:
                    print(f"Факультет: {stats[0]}, Студентов: {stats[1]}, "
                    f"Средняя оценка: {stats[2]:.1f}, Макс: {stats[3]}, Мин: {stats[4]}")

                    # 8. Практический пример: поиск студентов по курсу
                    def find_students_by_course(course_name):
                    """Найти всех студентов, изучающих конкретный курс"""
                    with closing(sqlite3.connect("university_advanced.db")) as conn:
                    cursor = conn.cursor()

                    query = '''
                    SELECT DISTINCT
                    s.name,
                    s.age,
                    g.grade,
                    g.semester
                    FROM students s
                    JOIN grades g ON s.id = g.student_id
                    JOIN courses c ON g.course_id = c.id
                    WHERE c.name = ?
                    ORDER BY g.grade DESC
                    '''

                    cursor.execute(query, (course_name,))
                    return cursor.fetchall()

                    # Пример использования
                    print("\n=== Поиск студентов по курсу 'Программирование' ===")
                    programming_students = find_students_by_course("Программирование")
                    for student in programming_students:
                    print(f"Студент: {student[0]}, Возраст: {student[1]}, Оценка: {student[2]}, Семестр: {student[3]}")