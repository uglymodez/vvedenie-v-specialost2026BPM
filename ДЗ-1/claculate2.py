def plus(a, b):
    return a + b

def minus(a, b):
    return a - b
    
def umnozh(a, b):
    return a * b

def delen(a, b):
    if b == 0:
        return "Ошибка деления на ноль"
    return a / b

a = float(input("Введите первое число: "))
b = float(input("Введите второе число: "))
operation = input("Выберите операцию (+, -, *, /): ")

if operation == "+":
    print("Результат:", plus(a, b))
elif operation == "-":
    print("Результат:", minus(a, b))
elif operation == "*":
    print("Результат:", umnozh(a, b))
elif operation == "/":
    print("Результат:", delen(a, b))
else:
    print("Нет такой операции")
