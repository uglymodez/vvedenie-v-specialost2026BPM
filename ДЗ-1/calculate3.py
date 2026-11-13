def calc(a, b, operation):
    if operation == '+':
        return a + b
    if operation == '-':
        return a - b
    if operation == '*':
        return a * b
    if operation == '/':
        return a / b
while True:
    operation = input('Введи операцию:')

    a = float(input('Введи число:'))
    b = float(input('Введи число:'))

    print(calc(a, b, operation))
