import calendar
import re
import sqlite3
import sys
from datetime import date, timedelta

from PyQt6.QtCore import QDate, QLocale, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from subscription_db import save_subscription


def calculate(buy=False):
    name = name_entry.text().strip()
    email = email_entry.text().strip()

    if len(name) < 2:
        QMessageBox.warning(window, "Ошибка", "Введите имя: минимум 2 символа.")
        return

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        QMessageBox.warning(window, "Ошибка", "Проверьте email. Пример: user@mail.ru")
        return

    accepted_terms = agreement.isChecked()
    if buy and not accepted_terms:
        QMessageBox.warning(window, "Ошибка", "Подтвердите согласие с условиями.")
        return

    selected = calendar_widget.selectedDate()
    start = date(selected.year(), selected.month(), selected.day())

    months = int(duration.currentText())
    tariff_name = tariff.currentText()
    total = prices[tariff_name] * months

    number = start.month - 1 + months
    end_year = start.year + number // 12
    end_month = number % 12 + 1

    # Если такого дня в месяце нет, берём последний день месяца.
    end_day = min(start.day, calendar.monthrange(end_year, end_month)[1])
    renewal = date(end_year, end_month, end_day)
    last_day = renewal - timedelta(days=1)

    if buy:
        try:
            save_subscription(
                name=name,
                email=email,
                start=start,
                last_day=last_day,
                tariff_name=tariff_name,
                months=months,
                total=total,
                accepted_terms=accepted_terms,
            )
        except sqlite3.Error as error:
            result.setText("Подписка не сохранена.")
            QMessageBox.warning(
                window, "Ошибка базы данных", f"Запись не сохранена.\n{error}"
            )
            return

        status = "Подписка оформлена (демо)"
    else:
        status = "Предварительный расчёт"

    result.setText(
        f"{status}\n"
        f"Клиент: {name} | {email}\n"
        f"Тариф: {tariff_name} | Срок: {months} мес.\n"
        f"Период: {start:%d.%m.%Y} — {last_day:%d.%m.%Y}\n"
        f"Итого: {total} руб. за весь срок. Деньги не списываются."
    )


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Кинотеатр — PyQt6")
window.resize(800, 520)

prices = {
    "Старт": 299,
    "Кино+": 499,
    "Семейный": 799,
}

main = QVBoxLayout(window)

title = QLabel("Подписка на кинотеатр")
title.setStyleSheet("font-size: 24px;")
main.addWidget(title)

body = QHBoxLayout()
main.addLayout(body)

calendar_widget = QCalendarWidget()
calendar_widget.setLocale(QLocale("ru_RU"))
calendar_widget.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
calendar_widget.setMinimumDate(QDate.currentDate())
calendar_widget.setMaximumDate(QDate(2099, 12, 31))
body.addWidget(calendar_widget)

form = QFormLayout()
body.addLayout(form)

name_entry = QLineEdit()
email_entry = QLineEdit()
form.addRow("Имя:", name_entry)
form.addRow("Email:", email_entry)

tariff = QComboBox()
tariff.addItems(list(prices))
form.addRow("Тариф:", tariff)

form.addRow(QLabel(
    "Старт — 299 руб./мес.\n"
    "Кино+ — 499 руб./мес.\n"
    "Семейный — 799 руб./мес."
))

duration = QComboBox()
duration.addItems(["1", "3", "6", "12"])
form.addRow("Срок, мес.:", duration)

agreement = QCheckBox("Согласен с условиями")
form.addRow(agreement)

calculate_button = QPushButton("Рассчитать")
buy_button = QPushButton("Оформить")
form.addRow(calculate_button, buy_button)

calculate_button.clicked.connect(lambda: calculate())
buy_button.clicked.connect(lambda: calculate(True))

result = QLabel("Заполните форму и нажмите «Рассчитать».")
result.setTextFormat(Qt.TextFormat.PlainText)
result.setWordWrap(True)
main.addWidget(result)

window.show()
sys.exit(app.exec())
