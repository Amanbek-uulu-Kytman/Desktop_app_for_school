import flet as ft
import sqlite3
import webbrowser

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('lessons.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            link TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Функция для получения всех уроков из базы данных
def get_lessons(filter_text=""):
    conn = sqlite3.connect('lessons.db')
    cursor = conn.cursor()
    if filter_text:
        cursor.execute("SELECT * FROM lessons WHERE name LIKE ?", (f"%{filter_text}%",))
    else:
        cursor.execute("SELECT * FROM lessons")
    lessons = cursor.fetchall()
    conn.close()
    return lessons

# Функция для добавления урока в базу данных
def add_lesson(name, link):
    conn = sqlite3.connect('lessons.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lessons (name, link) VALUES (?, ?)", (name, link))
    conn.commit()
    conn.close()

# Функция для удаления урока из базы данных
def delete_lesson(lesson_id):
    conn = sqlite3.connect('lessons.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
    conn.commit()
    conn.close()

def main(page: ft.Page):
    page.title = "Game Heaven Manager"
    init_db()  # Инициализация базы данных

    # Поля для ввода названия урока и ссылки
    txt_lesson_name = ft.TextField(label="Название урока", width=300)
    txt_lesson_link = ft.TextField(label="Ссылка на урок", width=300)

    # Поле для ввода фильтра
    txt_filter = ft.TextField(label="Фильтр по названию", width=300)

    # Кнопка для добавления урока
    btn_add_lesson = ft.ElevatedButton("Добавить урок", on_click=lambda e: add_lesson_to_db(e))

    # Кнопка для поиска
    btn_search = ft.IconButton(ft.icons.SEARCH, on_click=lambda e: update_lesson_table())

    # Таблица для отображения уроков
    lessons_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Ссылка")),
            ft.DataColumn(ft.Text("Действия")),
        ],
        rows=[],
    )

    # Функция для обновления таблицы уроков
    def update_lesson_table(e=None):
        lessons_table.rows.clear()  # Очистить текущие строки
        filter_text = txt_filter.value.strip()
        lessons = get_lessons(filter_text)  # Получить уроки из базы данных с фильтрацией
        for lesson in lessons:
            lesson_id, name, link = lesson
            lessons_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(name)),
                    ft.DataCell(ft.Text(link)),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(ft.icons.DELETE, data=str(lesson_id), on_click=delete_lesson_from_db),
                            ft.ElevatedButton("Посмотреть урок", on_click=lambda e, link=link: open_link(link))
                        ])
                    ),
                ])
            )
        lessons_table.update()

    # Функция для добавления урока
    def add_lesson_to_db(e):
        name = txt_lesson_name.value.strip()
        link = txt_lesson_link.value.strip()
        if name and link:
            add_lesson(name, link)  # Добавить урок в базу данных
            txt_lesson_name.value = ""  # Очистить поле ввода
            txt_lesson_link.value = ""  # Очистить поле ввода
            update_lesson_table()  # Обновить таблицу уроков
            page.update()

    # Функция для удаления урока
    def delete_lesson_from_db(e):
        lesson_id = int(e.control.data)
        delete_lesson(lesson_id)  # Удалить урок из базы данных
        update_lesson_table()  # Обновить таблицу уроков
        page.update()

    # Функция для открытия ссылки в браузере
    def open_link(link):
        webbrowser.open(link)  # Открыть ссылку в браузере

    # Добавляем элементы на страницу
    page.add(
        ft.Column([
            ft.Row([
                txt_lesson_name,
                txt_lesson_link,
                btn_add_lesson  # Добавляем кнопку добавления урока в строку
            ], alignment="center"),
            ft.Row([
                txt_filter,
                btn_search
            ], alignment="center"),
            lessons_table,
           
            ft.Text(" \nМбанк +996 773 23 72 04", size=12, weight="bold", color=ft.colors.GREEN)  # Имя автора
        ], alignment="center", horizontal_alignment="center") 
    )

    # Обновляем таблицу при запуске приложения
    update_lesson_table()

ft.app(target=main)
