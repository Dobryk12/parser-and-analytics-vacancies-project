import asyncio
import aiohttp
from dataclasses import dataclass
import re
import pandas as pd
import bs4
from constants import BASE_URL, BASE_URL_PY

list_of_works = []
list_of_vacs = []


@dataclass
class Vacancy:
    title: str
    city: str
    salary: str
    skills: list


async def get_vac_url():
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL_PY) as response:
            html = await response.text()
            soup = bs4.BeautifulSoup(html, "html.parser")
            number_of_pages = soup.select(".pagination.pagination-small.visible-xs-block > li")[1].text[-1]
            for page in range(1, int(number_of_pages) + 1):
                url = BASE_URL_PY + "?page=" + str(page)
                async with session.get(url) as response:
                    html = await response.text()
                    soup = bs4.BeautifulSoup(html, "html.parser")
                    works = soup.select(".card.card-hover.card-search.card-visited.wordwrap.job-link.js-job-link-blank")
                    for work in works:
                        vac_url = work.select_one(".add-bottom > h2 > a").get("href")
                        list_of_works.append(BASE_URL + vac_url)


async def get_vacs_all(list_of_works):
    async with aiohttp.ClientSession() as session:
        for work in list_of_works:
            async with session.get(work) as response:
                html = await response.text()
                soup = bs4.BeautifulSoup(html, "html.parser")
                title = get_title(soup)
                salary = get_salary(soup)
                city = get_city(soup)
                skills = get_skills(soup)
                vac = Vacancy(title, city, salary, skills)
                list_of_vacs.append(vac.__dict__)


def get_title(soup):
    return soup.find(id="h1-name").text


def get_salary(soup):
    salary_paragraph = soup.select_one("span.strong-500")
    salary = "Не вказана"
    if salary_paragraph:
        salary_text = salary_paragraph.parent.text
        if re.search(r'\d', salary_text) and "–" in salary_text:
            matches = re.findall(r'\d+', salary_text)
            if matches:
                salary = ''.join(matches)
                if len(salary) % 2 == 0:
                    salary = (salary[:(int(len(salary) / 2))] + " - " + salary[(int(len(salary) / 2)):])
                else:
                    salary = (salary[:int(len(salary) / 2)] + " - " + salary[int(len(salary) / 2):])
    return salary


def get_city(soup):
    city_paragraph = soup.select_one("li.text-indent.mt-sm span.glyphicon.glyphicon-map-marker.text-default.glyphicon-large")
    city = "Не вказано"
    if city_paragraph:
        city = city_paragraph.parent.text.split()[0]
        if "," in city:
            city = city[:-1]
    return city


def get_skills(soup):
    skills = soup.select(".mt-2xl.flex.flex-wrap > ul > li > span")
    skills_list = []
    for skill in skills:
        skills_list.append(skill.text)
    return skills_list


async def main():
    await get_vac_url()
    await get_vacs_all(list_of_works)
    df = pd.DataFrame(list_of_vacs)
    df.to_csv('vacancies.csv', index=False)

asyncio.run(main())

