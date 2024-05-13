import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('vacancies.csv')
city_counts = df['city'].value_counts()

plt.figure(figsize=(10, 6))
city_counts.plot(kind='pie', colors=['skyblue', 'lightgreen', 'lightcoral', 'orange', 'yellow'], autopct='%1.1f%%')
plt.title('Кількість вакансій за містами')
plt.axis('equal')  # Рівність вісей для зображення кола
plt.tight_layout()
plt.show()
