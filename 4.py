Python
                         Копировать
                    import sqlite3
                    from contextlib import closing

                    # 1. Создание базы данных и таблицы
                    def create_database():
                    """Создание базы данных и таблицы студентов"""
                    with closing(sqlite3.connect("university.db")) as conn:
                    cursor = conn.cursor()

                    # Создание таблицы
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    score REAL,
                    faculty TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                    ''')

                    # Создание индекса для быстрого поиска по имени
                    cursor.execute('''
                    CREATE INDEX IF NOT EXISTS idx_students_name
                    ON students(name)
                    ''')

                    conn.commit()
                    print("✅ База данных и таблица созданы")

                    # 2. Добавление тестовых данных
                    def add_sample_data():
                    """Добавление тестовых данных"""
                    with closing(sqlite3.connect("university.db")) as conn:
                    cursor = conn.cursor()

                    # Проверяем, есть ли уже данные
                    cursor.execute("SELECT COUNT(*) FROM students")
                    count = cursor.fetchone()[0]

                    if count == 0:
                    students = [
                    ("Иван Иванов", 20, 85.5, "Информатика"),
                    ("Мария Петрова", 21, 92.0, "Математика"),
                    ("Алексей Сидоров", 19, 78.5, "Физика"),
                    ("Елена Васильева", 22, 88.0, "Информатика"),
                    ("Дмитрий Николаев", 20, 76.5, "Математика")
                    ]

                    cursor.executemany(
                    "INSERT INTO students (name, age, score, faculty) VALUES (?, ?, ?, ?)",
                    students
                    )

                    conn.commit()
                    print(f"✅ Добавлено {len(students)} тестовых записей")

                    # 3. Обновление записи
                    def update_student_score(student_name, new_score):
                    """Обновление балла студента"""
                    with closing(sqlite3.connect("university.db")) as conn:
                    cursor = conn.cursor()

                    # Проверяем существование студента
                    cursor.execute("SELECT id, score FROM students WHERE name = ?", (student_name,))
                    student = cursor.fetchone()

                    if student:
                    student_id, old_score = student
                    print(f"🔄 Обновление студента {student_name}: {old_score} → {new_score}")

                    # Выполняем UPDATE
                    cursor.execute(
                    "UPDATE students SET score = ? WHERE id = ?",
                    (new_score, student_id)
                    )

                    if cursor.rowcount > 0:
                    conn.commit()
                    print(f"✅ Запись обновлена. Затронуто строк: {cursor.rowcount}")

                    # Показываем обновленную запись
                    cursor.execute(
                    "SELECT id, name, score FROM students WHERE id = ?",
                    (student_id,)
                    )
                    updated = cursor.fetchone()
                    print(f"Обновленная запись: ID={updated[0]}, Имя={updated[1]}, Балл={updated[2]}")
                    else:
                    print("⚠️ Запись не найдена")
                    else:
                    print(f"❌ Студент {student_name} не найден")

                    # Добавляем нового студента
                    cursor.execute(
                    "INSERT INTO students (name, score) VALUES (?, ?)",
                    (student_name, new_score)
                    )
                    conn.commit()
                    print(f"✅ Добавлен новый студент: {student_name}")

                    # 4. Получение всех студентов
                    def get_all_students():
                    """Получение всех студентов"""
                    with closing(sqlite3.connect("university.db")) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, name, age, score, faculty FROM students ORDER BY name")
                    return cursor.fetchall()

                    # 5. Поиск студентов по имени
                    def search_students_by_name(name_part):
                    """Поиск студентов по части имени"""
                    with closing(sqlite3.connect("university.db")) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                    "SELECT id, name, score FROM students WHERE name LIKE ?",
                    (f"%{name_part}%",)
                    )
                    return cursor.fetchall()

                    # 6. Пример использования
                    if __name__ == "__main__":
                    print("=== РАБОТА С SQLite ===")

                    # Создание базы данных
                    create_database()
                    add_sample_data()

                    print("\n=== Все студенты ===")
                    students = get_all_students()
                    for student in students:
                    print(f"ID: {student[0]}, Имя: {student[1]}, Возраст: {student[2]}, "
                    f"Балл: {student[3]}, Факультет: {student[4]}")

                    print("\n=== Обновление записи ===")
                    # Обновляем существующего студента
                    update_student_score("Иван Иванов", 90.0)

                    # Пытаемся обновить несуществующего студента (будет добавлен)
                    update_student_score("Новый Студент", 85.5)

                    print("\n=== Поиск студентов ===")
                    found = search_students_by_name("Иван")
                    for student in found:
                    print(f"Найден: {student[1]} (балл: {student[2]})")

                    print("\n=== Финальный список студентов ===")
                    students = get_all_students()
                    for student in students:
                    print(f"{student[1]} - {student[3]} баллов")

                    # 7. Дополнительные операции
                    def delete_student(student_id):
                    """Удаление студента по ID"""
                    with closing(sqlite3.connect("university.db")) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
                    conn.commit()
                    return cursor.rowcount

                    def get_student_statistics():
                    """Получение статистики по студентам"""
                    with closing(sqlite3.connect("university.db")) as conn:
                    cursor = conn.cursor()

                    cursor.execute("SELECT COUNT(*) FROM students")
                    total = cursor.fetchone()[0]

                    cursor.execute("SELECT AVG(score) FROM students")
                    avg_score = cursor.fetchone()[0]

                    cursor.execute("SELECT MAX(score) FROM students")
                    max_score = cursor.fetchone()[0]

                    cursor.execute("SELECT MIN(score) FROM students")
                    min_score = cursor.fetchone()[0]

                    return {
                    "total_students": total,
                    "average_score": avg_score,
                    "max_score": max_score,
                    "min_score": min_score
                    }

                    # 8. Пример транзакции
                    def update_multiple_students(updates):
                    """Обновление нескольких записей в транзакции"""
                    with closing(sqlite3.connect("university.db")) as conn:
                    try:
                    cursor = conn.cursor()

                    for student_id, new_score in updates:
                    cursor.execute(
                    "UPDATE students SET score = ? WHERE id = ?",
                    (new_score, student_id)
                    )

                    conn.commit()
                    print(f"✅ Обновлено {len(updates)} записей")

                    except sqlite3.Error as e:
                    conn.rollback()
                    print(f"❌ Ошибка: {e}. Изменения отменены.")