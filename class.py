class Calculator:
    def __init__ (self, first, second):
        self.first =first
        self.second = second

    def summator(self):
        return self.first +self.second

    def ymnozhator(self):
        return self.first * self.second

    def podelator(self):
        return self.first / self.second

    def vichitator(self):
        return self.first - self.second

class Kalories:
    def __init__ (self, product1, weight1=0):
        self.product1 = product1
        self.weight1 = weight1


    def molochka(self, percent_of_zhir):
        self.percent_of_zhir = percent_of_zhir
        if self.product1 == "молоко" and self.percent_of_zhir == 1:
            return f"Калории продукта{(self.weight1 / 100) * 41},Белки {(self.weight1 / 100) * 3.15}, Углеводы, {(self.weight1 / 100) * 4.8}, Жиры {(self.weight1 / 100) * 1}"
        if self.product1 == "молоко" and self.percent_of_zhir == 2.5:
                    return f"Калории продукта{(self.weight1 / 100) * 52},Белки {(self.weight1 / 100) * 3}, Углеводы, {(self.weight1 / 100) * 4.8}, Жиры {(self.weight1 / 100) * 2.5}"
        if self.product1 == "творог" and self.percent_of_zhir == 1.5:
                    return f"Калории продукта{(self.weight1 / 100) * 121},Белки {(self.weight1 / 100) * 15}, Углеводы, {(self.weight1 / 100) * 2}, Жиры {(self.weight1 / 100) * 0.8}"
        if self.product1 == "творог" and self.percent_of_zhir == 9:
                            return f"Калории продукта{(self.weight1 / 100) * 155},Белки {(self.weight1 / 100) * 15}, Углеводы, {(self.weight1 / 100) * 2}, Жиры {(self.weight1 / 100) * 9}"
        if self.product1 == "творог" and self.percent_of_zhir == 20:
                            return f"Калории продукта{(self.weight1 / 100) * 220},Белки {(self.weight1 / 100) * 15}, Углеводы, {(self.weight1 / 100) * 2}, Жиры {(self.weight1 / 100) * 18}"

    def ostalnoe(self):
        p = self.product1.lower().strip()
        w = self.weight1

        if "рисовая каша" in p:
            return f'Белки - {(w / 100) * 2.5}, Жиры - {(w / 100) * 0.8}, Углеводы - {(w / 100) * 17.0}, Калории - {(w / 100) * 89}'

        if "славяноч" in p:
            return f'Белки - {(w / 100) * 9}, Жиры - {(w / 100) * 12}, Углеводы - {(w / 100) * 25}, Калории - {(w / 100) * 245}'

        if "шаурма" in p:
            return f'Белки - {(w / 100) * 10.5}, Жиры - {(w / 100) * 12.5}, Углеводы - {(w / 100) * 18}, Калории - {(w / 100) * 220}'

        if "б-корпус" in p or "б корпус" in p:
            return f'Белки - {(w / 100) * 8}, Жиры - {(w / 100) * 10}, Углеводы - {(w / 100) * 22}, Калории - {(w / 100) * 210}'

        if "овсян" in p and "каша" in p:
            return f'Белки - {(w / 100) * 3.0}, Жиры - {(w / 100) * 1.7}, Углеводы - {(w / 100) * 15.0}, Калории - {(w / 100) * 88}'

        if "греч" in p:
            return f'Белки - {(w / 100) * 3.4}, Жиры - {(w / 100) * 0.6}, Углеводы - {(w / 100) * 17.1}, Калории - {(w / 100) * 90}'

    def myaso(self):

        if self.product1 == "жареная говядина":
            return f'Белки - {(self.weight1 / 100) * 32.7}, Жиры - {(self.weight1 / 100) * 28}, Углеводы - {(self.weight1 / 100) * 0}, Калории - {(self.weight1 / 100) * 384}'
        if self.product1 == "вареная говядина":
            return f'Белки - {(self.weight1 / 100) * 25.8}, Жиры - {(self.weight1 / 100) * 16.8}, Углеводы - {(self.weight1 / 100) * 0}, Калории - {(self.weight1/ 100) * 254}'
        if self.product1 == "жареная баранина":
            return f'Белки - {(self.weight1 / 100) * 32.7}, Жиры - {(self.weight1 / 100) * 28}, Углеводы - {(self.weight1 / 100) * 0}, Калории - {(self.weight1 / 100) * 384}'
        if self.product1 == "жареная баранина":
            return f'Белки - {(self.weight1 / 100) * 25}, Жиры - {(self.weight1 / 100) * 28}, Углеводы - {(self.weight1 / 100) * 0}, Калории - {(self.weight1 / 100) * 320}'
        if self.product1 == "жареная свинина":
            return f'Белки - {(self.weight1 / 100) * 24.6}, Жиры - {(self.weight1 / 100) * 21.4}, Углеводы - {(self.weight1 / 100) * 0}, Калории - {(self.weight1 / 100) * 259}'
        if self.product1 == "вареная свинина":
            return f'Белки - {(self.weight1 / 100) * 24}, Жиры - {(self.weight1 / 100) * 22}, Углеводы - {(self.weight1 / 100) * 0}, Калории - {(self.weight1 / 100) * 298}'
    
a = int(input("выберите калькулятор, 1 - обычный, 2 - кальукулятор калорий"))
if a == 1:
    c = int(input("Выберите одну из операций: 1 - сложение, 2 - вычитание, 3 - умножение, 4 - деление"))
    if c == 1:
        summa = Calculator(int(input()), int(input())) 
        print(summa.summator())
    if c == 2:
        razn = Calculator(int(input("Введите первое число: ")), int(input("Введите второе число: ")))
        print(razn.vichitator())
    if c == 3:
        ymnzh = Calculator(int(input("Введите первое число: ")), int(input("Введите второе число: ")))
        print(ymnzh.ymnozhator())
    if c == 4:
        delen = Calculator(int(input("Введите первое число: ")), int(input("Введите второе число: ")))
        print(delen.podelator())
if a == 2:
    d = int(input("выберите молочные продукты - 1, мясные - 2 или другое - 3: "))
    if d == 1:
        products = Kalories(input("молоко или творог"), int(input("вес в граммах: ")))
        print(products.molochka(int(input("Выбирите процент жира творога среди предложенных для молока: 1, 2.5, для творога 1.5, 9, 20"))))
    if d == 2:
        products = Kalories(input("выбирите вид мяса: жареная или вареная свинина, жареная или вареная свинина, жареная или вареная баранина: ").lower(), int(input("Вес в граммах")))
        print(products.myaso())
    if d == 3:
        products == Kalories(input("рисовая каша, комплексный обед из славяночки, шаурма за 300 вощле мисиса, комплексный обед в Б-корпусе, овсянная каша, гречневая крупа, выберите один из вариантов: "), int(input("Введите вес продукта в граммах:")))
        print(products.ostalnoe())
