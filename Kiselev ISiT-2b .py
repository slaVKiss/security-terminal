import sys
import sqlite3 as sq
from PyQt6.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QMessageBox)
from PyQt6.QtCore import QDateTime

base1=[("Алексеев","Илья","Алексеевич","23-Apr-1994","директор по информатизации","+79993456785","aleksee45@mail.ru","NULL","NULL"),
("Аржанов","Владислав","Александрович","27-Jan-1995","начальние отдела кадров","+79063194556","arhjanov12@yandex.ru","NULL","NULL"),
("Белоцерковец ","Дмитрий","Александрович","12-Sep-1983","менеджер","+79773332123","belotserkovets@gmail.com","NULL","NULL"),
("Богушев","Арсений","Александрович","09-Dec-1973","директор","+79264444334","Bogushev@mail.ru","NULL","NULL"),
("Гундарова","Софья","Анатольевна","30-Nov-1995","менеджер","+79256789012","Gundarova@yandex.ru","NULL","NULL"),
("Долженков","Борис","Алексеевич","23-Jun-2002","курьер","+79003196748","Dolzhenkov@gmail.com","NULL","NULL"),
("Журавова","Ангелина","Сергеевна","17-Aug-2002","специалист по корреспонденции","+79836571245","Zhuravova@gmail.com","NULL","NULL"),
("Клевцова","Варвара","Андреевна","15-Oct-2002","секретарь","+79023672156","Klevtsova@gmail.com","NULL","NULL"),
("Коваленко","Вероника","Александровна","17-Jul-1997","менеджер","+79271285522","Kovalenko@gmail.com","NULL","NULL"),
("Королев","Платон","Валеорьевич","13-Mar-1993","главный бухгалтер","+79773045689","Korolev@gmail.com","NULL","NULL"),
("Кубышкин","Роман","Евгеньевич","10-Oct-1985","менеджер по технологии","+79013219045","Kubyshkin@gmail.com","NULL","NULL"),
("Макаренко","Константин","Викторович","11-Nov-1984","бизнес аналитик","+79992341289","Makarenko@gmail.com","NULL","NULL"),
("Мартиросов","Артемий","Артурович","01-Feb-1974","smm - менеджер","+79027893459","Martirosov@gmail.com","NULL","NULL"),
("Мелкумян","Роберт","Робертович","16-May-1993","маркетолог","+79982341290","Melkumyan@gmail.com","NULL","NULL"),
("Олейник","Ольга","Викторовна","18-Jun-1993","руководитель проекта","+79762349987","Oleinik@gmail.com","NULL","NULL"),
("Полюцкий","Александр","Сергеевич","19-Jan-1981","юрист-консультант","+79673421894","Polyutsky@gmail.com","NULL","NULL"),
("Рустамов","Иброхим","Рустамович","29-Oct-1982","зав.хозяйством","+79231782392","Rustamov@gmail.com","NULL","NULL"),
("Рябцева","Алена","Александровна","14-Nov-1982","бухгалтер","+79321743981","Ryabtseva@gmail.com","NULL","NULL"),
("Саберова","Динара","Равилевна","28-Dec-1994","главный юрист","+79992341084","Saberova@gmail.com","NULL","NULL"),
("Сафонова","Ирина","Ивановна","15-Jul-1983","делопроизводитель","+79253419861","Safonov@gmail.com","NULL","NULL"),
("Стронина","София","Евгеньевна","31-Mar-2002","секретарь","+79162381629","Stronina@gmail.com","NULL","NULL"),
("Тарасов","Степан","Павлович","06-Jun-1996","менеджер","+79152371823","Тарасов@gmail.com","NULL","NULL"),
("Чекменёв","Кирилл","Андреевич","02-Aug-1998","дизайнер","+79172361959","Chekmenev@gmail.com","NULL","NULL"),
("Чернов","Максим","Дмитриевич","23-Dec-1999","аналитик","+79293652732","Chernov@gmail.com","NULL","NULL"),
("Шарофидинова","Ирода","Отабек","21-Mar-1991","уборщица","+79002893276","Sharofidinov@gmail.com","NULL","NULL"),
("Шундрик","Егор","Максимович","07-Apr-1992","расчетчик","+79281123119","Shundrick@gmail.com","NULL","NULL"),
("Шушняев","Никита","Максимовна","09-Sep-1991","сметчик","+79031732861","Shushnyaev@gmail.com","NULL","NULL")]


def create_db():
    with sq.connect("company.db") as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees(
                id INTEGER PRIMARY KEY,
                last_name TEXT NOT NULL,
                first_name TEXT NOT NULL,
                middle_name TEXT NOT NULL,
                birth_date TEXT,
                position TEXT,
                phone TEXT,
                email TEXT,
                time_in TEXT,
                time_out TEXT) """)


        cur.executemany("""
            INSERT INTO employees (
                last_name, first_name, middle_name, birth_date, position,
                phone, email, time_in, time_out)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", base1)
        con.commit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initDB()

    def initUI(self):
        self.setWindowTitle("КПП Охранника")


        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText("Введите фамилию сотрудника")


        self.btn_entry = QPushButton("Вход", self)
        self.btn_exit = QPushButton("Выход", self)


        self.btn_entry.clicked.connect(self.register_entry)
        self.btn_exit.clicked.connect(self.register_exit)


        layout = QVBoxLayout()
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.btn_entry)
        layout.addWidget(self.btn_exit)

        self.setLayout(layout)

    def initDB(self):
        self.con = sq.connect("company.db")
        self.cur = self.con.cursor()

    def register_entry(self):
        self.register_time("time_in")

    def register_exit(self):
        self.register_time("time_out")

    def register_time(self, time_field):
        last_name = self.last_name_input.text().strip()
        if last_name:
            current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
            self.cur.execute(f"""
                UPDATE employees
                SET {time_field} = ?
                WHERE last_name = ?
                """, (current_time, last_name))
            self.con.commit()
            if self.cur.rowcount == 0:
                QMessageBox.warning(self, "Ошибка", "Сотрудник не найден.")
            else:
                QMessageBox.information(self, "Регистрация", f"Время {('прихода' if time_field == 'time_in' else 'ухода')} зарегистрировано.")
        else:
            QMessageBox.warning(self, "Ошибка", "Фамилия сотрудника не введена.")

    def closeEvent(self, event):
        self.con.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    create_db()
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
