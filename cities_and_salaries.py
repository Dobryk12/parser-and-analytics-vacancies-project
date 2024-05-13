import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('vacancies.csv')

df = df[df['salary'] != 'Не вказана']


def format_salary_range(salary_range):
    if '–' in salary_range:
        return salary_range
    else:
        lower, upper = salary_range.split(' - ')
        average_salary = (int(lower) + int(upper)) / 2
        return f"{int(average_salary)} - {int(average_salary)}"


df['salary'] = df['salary'].apply(format_salary_range)

city_salary_count = df.groupby('city')['salary'].count().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
city_salary_count.plot(kind='bar', color='skyblue')
plt.title('Кількість вакансій зі зазначеною зарплатою за містами')
plt.xlabel('Місто')
plt.ylabel('Кількість вакансій')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
