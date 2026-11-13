

def firstlvl(vvod_polsovatel=0):
    print("Справочная информация: ")
    print("str.lower() в Python возвращает копию строки, в которой все символы переведены в нижний регистр")
    print("str.upper() в Python преобразует все символы строки в верхний регистр")
    print("str.capitalize() в Python делает первую букву всей строки заглавной, а все остальные буквы переводит в нижний регистр")
    print("пример: test1 = str('пРиВет Мир'), test1.lower() = str('привет мир')" )
    print("пример: test2 = str('пРиВет Мир'), test2.upper() = str('ПРИВЕТ МИР')" )
    print("пример: test3 = str('пРиВет Мир'), test3.lower() = str('Привет мир')" )
    n = input("Выбирите интересующий метод: ")
    if n == "str.lower()":
        huh = input("введите свою строку: ")
        return f'Ваш результат: {huh.lower()}'
    if n == "str.upper()":
        huh = input("введите свою строку: ")
        return f'Ваш результат: {huh.upper()}'
    if n == "str.capitalize()":
        huh = input("введите свою строку: ")
        return f'Ваш результат: {huh.capitalize()}'


#print(firstlvl())


def secondlvl():
    print("Справочная информация: ")
    print("find() - ищет первое вхождение подстроки sub в строке")
    print("count() - ищет количество вхождение подстроки sub в строке")
    print("replace() - заменяет старую подстроку old на новую new во всей изначальной стрроке")
    print("index(sub)) - выводит индекс первого вхождения подстроки sub, на определенном участке строки")
    print("пример: test1 = str('пРиВет Мир'), test1.find(Мир) = 7" )
    print("пример: test2 = str('пРиВет Мир'), test2.count('и') = 2" )
    print("пример: test3 = str('пРиВет Мир'), test3.replace('и', 'у') = str('Прувет мур')" )
    print("пример: test4 = str('пРиВет Мир'), test4.index('и', 5) = 8" )
    n = input("Выберите интересующий вас метод: ")
    if n == "str.find()":
        juk = input("Введите свою строку: ")
        dub = input("Введите подстроку, которую вы хотите найти: ")
        return f'Ваш результат{juk.find(str(dub))}'
    if n == "str.count()":
            juk = input("Введите свою строку: ")
            dub = input("Введите подстроку, вхождения которой вы хотите подсчитать: ")
            return f'Ваш результат{juk.count(str(dub))}'
    if n == "str.replace()":
            juk = input("Введите свою строку: ")
            lol = input("Введите подстроку, которую вы хотите заменить: ")
            dub = input("Введите подстроку,на которую вы хотите заменить: ")
            return f'Ваш результат: {juk.replace(str(lol), str(dub))}'
    if n == "str.index()":
        juk = input("Введите свою строку: ")
        dub = input("Введите подстроку,которую вы хотите найти: ")
        first = int(input("при необходимости введите с какого индекса начать, если это не нужно введите 0: "))
        second = int(input("при необходимости введите с какого индекса начать, если это не нужно ничего не вводите"))
        return f'Ваш результат{juk.replace(str(dub), first, second)}'


def thirdlvl():
    print("Справочная информация: ")
    print("split() - используется для разибение строки или списка на более маленькие строки по заданному разделителю ")
    print("join() - объединяет элементы итерируемого объекта (например, списка или кортежа) в одну общую строку, используя заданный разделитель")
    print("пример test1 = 'один два три', test1.split( ) = 'один, два, три'")
    print("пример test2 = 'один, test3 = 'два', io = ''.join([test2, test3]), io = 'один два'")
    n = input("Выберите интересующий вас метод: ")
    if n == "str.split()":
         bazar = input("Введите свою строку: ")
         vokzal = input("Введите разделитель:")
         return bazar.split(f"{vokzal}")
    elif n == "str.join()":
         s = input("Введите первую из двух строк: ")
         d = input("Введите вторую строку: ")
         io = [s, d]
         results = "".join(io)
         return results


def fourthlvl():
     print("Справочная информация: ")
     print("isdigit() - проверяет являются ли все символы строки цифрами или нет, возвращает булевое значение(True - если являются , False - если не являются)")
     print("isalpha() - проверяет являются ли все символы строки буквами или нет, возвращает булевое значение(True - если являются , False - если не являются)")
     print("strip() - очищает строку по краям, чтобы дальше с ней было удобнее работать. Что именно нужно удалить, определяет программист")
     print("format() - позволяет вводить в готовую строку недостающие символы/слова в специально отведенные для этого места.")
     print("пример использования isdigit(): test1 = 12efrffarf12313 , test1.isdigit() = False")
     print("пример использования isalpha(): test2 = qfwpvmwekpvmwevKifeivmKKJIC, test2.isalpha() = True")
     print("пример использования strip(): test3 = '  opa vperedi kopbI  ', test3.lstrip() = 'opa vperedi kopbI  ', test3.rstrip() ='  opa vperedi kopbI', test3.strip = 'opa vperedi kopbI' ")
     print("пример использования format(): test4 = Hello, {}!'.format('Vasya''), test4 = Hello, Vasya!'")
     n = input("Выберите интересующий вас метод: ")
     if n == "str.isdigit()":
          rama = input("Введите вашу строку: ")
          return rama.isdigit()
     elif n == "str.isalpha()":
          dva = input("Введите интересующую вас строку: ")
          return dva.isalpha()
     elif n == "str.format()":
          vandamma = input("Введите интересующую вас строку({} - обозначьте место куда неоходимо будет вставлять подстроку): ")
          huh = input("Введите вставляемую подстроку: ")
          return vandamma.format(f"{huh}")
     elif n == "str.strip()":
          vibor = input("Выберите какой вид метода вас интересует: rstrip(), lstrip(), strip(): ")
          if vibor == "rstrip()":
               j = input("Введите вашу строку: ")
               return j.rstrip()
          elif vibor == "lstrip()":
               f = input("Введите вашу строку: ")
               return f.lstrip()
          elif vibor == "strip()":
               b = input("Введите вашу строку: ")
               return b.strip()


def fifthlvl():
    print("Поиграемся с пройденными методами))" \
    "Введите строку и выберите методы, которые вы хотите к ней применить ")
    ds = int(input("Выберите сколько методов вы хотите использовать: "))
    aaa = input("Введите форматируемую строку: ")
    
    list = []
    konec = []
    while (ds > 0):
         y = input("Вводите методы в столбец:")
         list.append(y)
         ds -=1
    for i in list:
         method = getattr(aaa, i, None)
         if callable(method):
              konec.append(f"Резульат и название метода: {method()} - .{i}()")
         else:
              konec.append("Такого метода не существует!!!!!")

    return "\n".join(konec)
 
g = int(input("Выберите интересующий вас уровень 1 - 5: "))
if g == 1:
    print(firstlvl())
elif g == 2:
    print(secondlvl())
elif g == 3:
    print(thirdlvl())
elif g == 4:
    print(fourthlvl())
elif g == 5:
     print(fifthlvl())
else:
    print("Вы ввели недопустимый номер уровня, gg")
