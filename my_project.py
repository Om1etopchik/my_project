#Импорты
import tkinter as tk
from tkinter import ttk
import sqlite3

#Создаем главное окно
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        #Инициализируем главное окно
        self.init_main()
        self.db = db
        #Делаем запрос на показ базы данных 
        self.view_records()

    #Настройка главного окна
    def init_main(self):
        #Создание фрейма
        frame = tk.Frame(bg="#d7d8c8", bd=2)
        frame.pack(side=tk.TOP, fill=tk.X)

        #Картинка и кнопка функции добавления
        self.add_img = tk.PhotoImage(file=r"Synergy\project\img\add.png")
        btn_open_dialog = tk.Button(frame, bg="#d7d8c8", bd=0, image=self.add_img, command=self.open_form)
        btn_open_dialog.pack(side=tk.LEFT)

        #Картинка и кнопка функции обновления
        self.update_png=tk.PhotoImage(file=r"Synergy\project\img\update.png")
        btn_edit_dialog = tk.Button(frame, bg="#d7d8c8", bd=0, image=self.update_png, command=self.open_update_form)
        btn_edit_dialog.pack(side=tk.LEFT)

        #Картинка и кнопка функции удаления
        self.delete_png=tk.PhotoImage(file=r"Synergy\project\img\delete.png")
        btn_delete = tk.Button(frame, bg="#d7d8c8", bd=0, image=self.delete_png, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        #Картинка и кнопка функции поиска
        self.search_png=tk.PhotoImage(file=r"Synergy\project\img\search.png")
        btn_search = tk.Button(frame, bg="#d7d8c8", bd=0, image=self.search_png, command=self.open_search_form)
        btn_search.pack(side=tk.LEFT)

        #Картинка и кнопка обновления
        self.refresh_png=tk.PhotoImage(file=r"Synergy\project\img\refresh.png")
        btn_refresh = tk.Button(frame, bg="#d7d8c8", bd=0, image=self.refresh_png, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        #Создании базы
        self.tree = ttk.Treeview(self, columns=("ID", "name", "tel", "email", "salary"), height=45, show="headings")
        
        #Прокрутка для данных из базы данных
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        
        #Создание колонок
        self.tree.column('ID', width=30, anchor="center")
        self.tree.column('name', width=300, anchor="center")
        self.tree.column('tel', width=150, anchor="center")
        self.tree.column('email', width=150, anchor="center")
        self.tree.column('salary', width=150, anchor="center")

        #Переименовка для пользователей
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="З/П")

        #Расположения по левой стороне
        self.tree.pack(side=tk.LEFT)

    #Функция для вызова класса
    def open_form(self):
        Newwindow(root)

    #Функция для вызова класса
    def open_update_form(self):
        Update()
    
    #Функция для вызова класса
    def open_search_form(self):
        Search()

    #Записи
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    def search_record_form(self, name):
        #Очищение переменной от левой и правой части
        name = ('%' + name + '%')

        #Запрос на отдачу всех данных где "name" включает переменную name из таблицы
        self.db.cur.execute('''SELECT * FROM my_project WHERE name LIKE ?''', (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]

        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    #Функция обновления записи
    def update_record_form(self, name, tel, email, salary):
        #Запрос на обновление
        self.db.cur.execute('''UPDATE my_project SET name = ?, tel = ?, email = ?, salary = ? WHERE id = ?''', (name, tel, email, salary, self.tree.set(self.tree.selection() [0], "#1"),))
        #Сохранение
        self.db.conn.commit()

        self.view_records()

    #Функция удаления записи
    def delete_record(self):
        #Запрос с циклом на удаление
        for select_item in self.tree.selection():
            self.db.cur.execute('''DELETE FROM my_project WHERE id = ?''', self.tree.set(select_item, "#1"))
        #Сохранение
        self.db.conn.commit()

        self.view_records()

    #Выбираем все записи и показываем
    def view_records(self):
        #Запрос на отдачу всех данных из таблицы
        self.db.cur.execute('SELECT * FROM my_project')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

#Класс нового окна
class Newwindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        #Инициализируем новое окно
        self.init_newwindow()
        self.view = application

    #Настройка нового окна
    def init_newwindow(self):
        #Заглавие
        self.title("Добавить")
        #Размеры
        self.geometry("450x250")
        #Позволение измения окна
        self.resizable(False, False)
        #Чтобы главное окно не закрывалось до закрытие последующего окна
        self.grab_set()
        #Сфокусировать внимение на выделенном
        self.focus_set()

        #Делаем форму данных
        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=50, y=50)
        label_tel = tk.Label(self, text="Телефон")
        label_tel.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail")
        label_sum.place(x=50, y=110)
        label_sal = tk.Label(self, text="Заработная плата")
        label_sal.place(x=50, y=140)

        #Делаем поля ввода
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)
        self.entry_sum = ttk.Entry(self)
        self.entry_sum.place(x=200, y=110)
        self.entry_sal = ttk.Entry(self)
        self.entry_sal.place(x=200, y=140)

        #Делаем кнопку закрытия
        self.btn_exit = tk.Button(self, text="Закрыть", command=self.destroy)
        self.btn_exit.place(x=300, y=170)

        #Делаем кнопку для отправки данных в базу данных и отправляем значения
        self.btn_add = tk.Button(self, text="Добавить")
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind("<Button-1>", lambda event: self.view.records(self.entry_name.get(), self.entry_tel.get(), self.entry_sum.get(), self.entry_sal.get()))
        #add нужен для дполонительной функции
        self.btn_add.bind("<Button-1>", lambda event: self.destroy(), add="+")

#Класс нового окна для обновления
class Update(Newwindow):
    def __init__(self):
        super().__init__(root)
        self.init_update()
        self.view = application
        self.db = db
        self.default_data()

    def init_update(self):
        #Заглавие
        self.title("Редактирование сотрудника")
        btn_edit=ttk.Button(self, text="Редактировать")
        #Расположение
        btn_edit.place(x=205, y=170)
        #Определенные действие на кнопку 1
        btn_edit.bind("<Button-1>", lambda event: self.view.update_record_form(self.entry_name.get(), self.entry_tel.get(), self.entry_sum.get(), self.entry_sal.get()))
        #Определенные действие на кнопку 1
        btn_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.btn_add.destroy()

    #Функция для вывода в поля ввода значения
    def default_data(self):
        #Запрос на отдачу всех данных где определенный id из таблицы
        self.db.cur.execute('''SELECT * FROM my_project WHERE id = ?''', (self.view.tree.set(self.view.tree.selection() [0], "#1"),))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_sum.insert(0, row[3])
        self.entry_tel.insert(0, row[2])
        self.entry_sal.insert(0, row[4])

#Класс нового окна для поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = application
    
    def init_search(self):
        self.title("Поиск сотрудника")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Имя")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=105, y=50)
        btn_search.bind("<Button-1>", lambda event: self.view.search_record_form(self.entry_search.get()))
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")

#Класс базы данных
class DB:
    #Инициализируем бд, чтобы не позникало ошибок, делаем ее каждый раз
    def __init__(self):
        #Создание файла базы данных
        self.conn = sqlite3.connect("my_project.db")
        self.cur = self.conn.cursor()
        #Запрос на создание таблицы
        self.cur.execute('''CREATE TABLE IF NOT EXISTS my_project(
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         tel TEXT,
                         email TEXT,
                         salary INTEGER
        )''')
        #Сохранение
        self.conn.commit()

    #Добавка значений в бд через поле ввода в новой окне
    def insert_data(self, name, tel, email, salary):
        self.cur.execute('''INSERT INTO my_project (name, tel, email, salary) VALUES (?,?,?,?);''', (name, tel, email, salary))
        #Сохранение
        self.conn.commit()

if __name__ == "__main__":
    #Создание окна
    root = tk.Tk()
    db = DB()
    application = Main(root)
    application.pack()

    #Заглавие
    root.title("Список сотрудников компании")
    #Размеры
    root.geometry("780x450")
    #Позволение измения окна
    root.resizable(False, False)
    #Запуск приложения
    root.mainloop()

