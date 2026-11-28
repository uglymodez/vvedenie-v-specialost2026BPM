import calendar
import re
import sqlite3
import tkinter as tk
from datetime import date, datetime, timedelta
from tkinter import messagebox, ttk

from subscription_db import save_subscription


def choose_day(day):
    date_entry.delete(0, tk.END)
    date_entry.insert(0, date(year, month, day).strftime("%d.%m.%Y"))


def show_month():
    for widget in days_frame.winfo_children():
        widget.destroy()

    month_label.config(text=f"{month:02d}.{year}")

    weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    for column, name in enumerate(weekdays):
        tk.Label(days_frame, text=name).grid(row=0, column=column)

    for row, week in enumerate(calendar.monthcalendar(year, month), start=1):
        for column, day in enumerate(week):
            if day != 0:
                button = tk.Button(
                    days_frame,
                    text=day,
                    width=4,
                    command=lambda d=day: choose_day(d),
                )
                button.grid(row=row, column=column, padx=2, pady=2)

                if date(year, month, day) < date.today():
                    button.config(state="disabled")


def change_month(step):
    global year, month

    number = year * 12 + month - 1 + step
    new_year, new_month = divmod(number, 12)

    if 1900 <= new_year <= 2099:
        year = new_year
        month = new_month + 1
        show_month()


def calculate(buy=False):
    name = name_entry.get().strip()
    email = email_entry.get().strip()

    if len(name) < 2:
        messagebox.showerror("Ошибка", "Введите имя: минимум 2 символа.")
        return

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        messagebox.showerror("Ошибка", "Проверьте email. Пример: user@mail.ru")
        return

    try:
        start = datetime.strptime(date_entry.get(), "%d.%m.%Y").date()
    except ValueError:
        messagebox.showerror("Ошибка", "Введите существующую дату: ДД.ММ.ГГГГ.")
        return

    if start < date.today() or start.year > 2099:
        messagebox.showerror("Ошибка", "Дата должна быть от сегодня до 31.12.2099.")
        return

    accepted_terms = agreement.get()
    if buy and not accepted_terms:
        messagebox.showerror("Ошибка", "Подтвердите согласие с условиями.")
        return

    months = int(duration.get())
    tariff_name = tariff.get()
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
            result.config(text="Подписка не сохранена.")
            messagebox.showerror(
                "Ошибка базы данных", f"Запись не сохранена.\n{error}"
            )
            return

        status = "Подписка оформлена (демо)"
    else:
        status = "Предварительный расчёт"

    result.config(text=(
        f"{status}\n"
        f"Клиент: {name} | {email}\n"
        f"Тариф: {tariff_name} | Срок: {months} мес.\n"
        f"Период: {start:%d.%m.%Y} — {last_day:%d.%m.%Y}\n"
        f"Итого: {total} руб. за весь срок. Деньги не списываются."
    ))


root = tk.Tk()
root.title("Кинотеатр — Tkinter")
root.geometry("800x590")
root.minsize(800, 590)

prices = {
    "Старт": 299,
    "Кино+": 499,
    "Семейный": 799,
}

year = date.today().year
month = date.today().month

tk.Label(root, text="Подписка на кинотеатр", font=("Arial", 20)).pack(pady=15)

body = tk.Frame(root)
body.pack(padx=15, fill="x")

left = tk.LabelFrame(body, text="Выберите дату начала", padx=10, pady=10)
left.pack(side="left", anchor="n")

navigation = tk.Frame(left)
navigation.pack(fill="x")

tk.Button(navigation, text="<", command=lambda: change_month(-1)).pack(side="left")
tk.Button(navigation, text=">", command=lambda: change_month(1)).pack(side="right")

month_label = tk.Label(navigation)
month_label.pack()

days_frame = tk.Frame(left)
days_frame.pack(pady=10)

right = tk.Frame(body)
right.pack(side="right", padx=15)

tk.Label(right, text="Имя").pack(anchor="w")
name_entry = ttk.Entry(right, width=35)
name_entry.pack(pady=(0, 7))

tk.Label(right, text="Email").pack(anchor="w")
email_entry = ttk.Entry(right, width=35)
email_entry.pack(pady=(0, 7))

tk.Label(right, text="Дата начала: ДД.ММ.ГГГГ").pack(anchor="w")
date_entry = ttk.Entry(right, width=35)
date_entry.insert(0, date.today().strftime("%d.%m.%Y"))
date_entry.pack(pady=(0, 7))

tk.Label(
    right,
    text="Тариф: Старт 299 / Кино+ 499 / Семейный 799 руб./мес.",
    wraplength=300,
).pack()

tariff = ttk.Combobox(right, values=list(prices), state="readonly", width=32)
tariff.current(0)
tariff.pack(pady=5)

tk.Label(right, text="Срок в месяцах").pack(anchor="w")
duration = ttk.Combobox(right, values=[1, 3, 6, 12], state="readonly", width=32)
duration.current(0)
duration.pack(pady=5)

agreement = tk.BooleanVar()
tk.Checkbutton(right, text="Согласен с условиями", variable=agreement).pack()

buttons = tk.Frame(right)
buttons.pack(pady=8)

tk.Button(buttons, text="Рассчитать", command=calculate).pack(side="left", padx=5)
tk.Button(buttons, text="Оформить", command=lambda: calculate(True)).pack(side="left")

result = tk.Label(
    root,
    text="Заполните форму и нажмите «Рассчитать».",
    justify="left",
    wraplength=750,
    font=("Arial", 11),
)
result.pack(padx=15, pady=15, anchor="w")

show_month()
root.mainloop()
