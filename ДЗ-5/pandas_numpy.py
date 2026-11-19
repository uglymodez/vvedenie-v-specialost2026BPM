import numpy as np
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

df = pd.read_csv("tested.csv")
orig_shape = df.shape
n = int(input("n = "))
print(df.head(n))
print(df.tail(5))
print("Строк, столбцов:", df.shape)
print(list(df.columns))
print(df.dtypes)
num = ["Age", "SibSp", "Parch", "Fare"]
cat = ["Survived", "Pclass", "Sex", "Embarked", "Cabin", "Name", "Ticket"]
print("Числовые:", num, "\nКатегориальные:", cat)
print(df[num].agg(["mean", "median", "min", "max", "std"]).T)
print(df["Pclass"].value_counts().sort_index())
print("Уникальных Embarked:", df["Embarked"].nunique())

miss = df.isna().sum()
print(miss)
print((miss / len(df) * 100).round(2))
print("Макс. пропусков:", miss.idxmax(), miss.max())


def age_stats(s):
    return pd.Series({"Среднее": s.mean(), "Медиана": s.median(),
                      "Минимум": s.min(), "Максимум": s.max(),
                      "Std": s.std(), "Известных значений": s.count()})


before = age_stats(df["Age"])
df["Age"] = df["Age"].fillna(df["Age"].median())
after = age_stats(df["Age"])
print(pd.DataFrame({"До": before, "После": after}).round(3))

df = df.dropna(subset=["Embarked"])
cabin_pct = df["Cabin"].isna().mean() * 100
print(f"Пропусков в Cabin: {cabin_pct:.1f}%")
if cabin_pct > 50:
    df = df.drop(columns="Cabin")
print(df.isna().sum())
print("До:", orig_shape, "После:", df.shape)

s = df["Survived"].to_numpy()
sex = df["Sex"].to_numpy()
age = df["Age"].to_numpy(float)
fare = df["Fare"].to_numpy(float)
m, f = sex == "male", sex == "female"
alive, dead = s == 1, s == 0

print(f"Выжили всего: {s.mean() * 100:.2f}%")
print(f"Мужчины: {s[m].mean() * 100:.2f}%, женщины: {s[f].mean() * 100:.2f}%")
print(f"Ср. возраст: мужчины {age[m].mean():.2f}, женщины {age[f].mean():.2f}")
res = pd.DataFrame({
    "Мужчины": [s[m].mean() * 100, age[m].mean(), age[m & alive].mean(), age[m & dead].mean()],
    "Женщины": [s[f].mean() * 100, age[f].mean(), age[f & alive].mean(), age[f & dead].mean()],
}, index=["Выжили, %", "Ср. возраст", "Ср. возраст выживших", "Ср. возраст погибших"]).round(2)
print(res)
print(f"Билет: min {np.nanmin(fare):.2f}, max {np.nanmax(fare):.2f}, "
      f"mean {np.nanmean(fare):.2f}")
print(f"Std возраста: {np.std(age, ddof=1):.2f}")

f1 = df[(df.Sex == "male") & (df.Age > 30) & (df.Pclass == 1)]
print(len(f1))
print(f1.head(10))
f2 = df[(df.Age < 18) | ((df.Sex == "female") & (df.Survived == 1))]
print(len(f2))
f3 = df[(df.Pclass == 3) & (df.Fare > df.loc[df.Pclass == 3, "Fare"].mean())]
print(len(f3))
f4 = df[df.Age.between(20, 40) & (df.Embarked == "S")]
print(len(f4))

stats = df.groupby(["Pclass", "Sex"]).agg(
    Количество=("Survived", "size"), Средний_возраст=("Age", "mean"),
    Выжившие_pct=("Survived", lambda x: x.mean() * 100),
    Средний_билет=("Fare", "mean")).round(2)
print(stats)
print(df.groupby("Embarked")["Survived"].agg(
    Количество="size", Выжившие_pct=lambda x: x.mean() * 100).round(2))
by_class = df.groupby("Pclass")["Survived"].mean() * 100
print("Лучший класс:", by_class.idxmax(), f"({by_class.max():.2f}%)")

df = df.reset_index(drop=True)
df.to_csv("titanic_processed.csv", index=False)
stats.to_csv("titanic_statistics.csv")
check = pd.read_csv("titanic_processed.csv")
print("Совпадает:", check.shape == df.shape,
      check.isna().sum().equals(df.isna().sum()))
print(check.head())

