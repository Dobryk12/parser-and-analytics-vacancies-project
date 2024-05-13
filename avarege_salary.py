import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('vacancies.csv')


df = df[df['salary'] != 'Не вказана']


def format_salary_range(salary_range):
    if '–' in salary_range:
        lower, upper = map(int, salary_range.split(' - '))
        return (lower + upper) / 2
    elif '-' in salary_range:
        lower, upper = map(int, salary_range.split(' - '))
        return (lower + upper) / 2
    else:
        return int(salary_range)


df['salary'] = df['salary'].apply(format_salary_range)

city_salary_avg = df.groupby('city')['salary'].mean().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
city_salary_avg.plot(kind='bar', color='skyblue')
plt.title('Середня зарплата за містами')
plt.xlabel('Місто')
plt.ylabel('Середня зарплата')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()