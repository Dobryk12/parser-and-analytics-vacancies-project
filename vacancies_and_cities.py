import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('vacancies.csv')
city_counts = df['city'].value_counts()

plt.figure(figsize=(10, 6))
city_counts.plot(kind='bar', color='skyblue')
plt.title('Кількість вакансій за містами')
plt.xlabel('Місто')
plt.ylabel('Кількість вакансій')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
