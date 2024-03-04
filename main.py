import csv
import requests
from fake_useragent import UserAgent

ua = UserAgent()
filename = 'vacancies.csv'

def get_vacansies(keyword: str, pages: int = 5):
    headers = ['Наименование вакансии', 'Зарплата', 'Наличие тестового задания', 'Дата публикации', 'Организация',
               'URL-ссылка']
    with open(filename, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(headers)

    for number_of_page in range(pages):
        url = 'https://api.hh.ru/vacancies'
        headers = {
            "User-Agent": ua.random,
        }
        params = {
            "page": number_of_page,  # Номер страницы
            "per_page": 100,  # Количество элементов на странице
            "text": keyword,  # Ключевые слова в вакансии
            "experience": 'noExperience',  # Опыт работы
            "area": 2  # Область
        }

        response = requests.get(url, headers=headers, params=params).json()
        data = response["items"]

        name = [i['name'] for i in data]  # Название вакансии
        salary = [f"{i['salary']['from']}-{i['salary']['to']}" if i['salary'] != None else 'None' for i in
                  data]  # Зарплата
        employer = [i['employer']['name'] for i in data]  # Работодатель
        test = ['Да' if i['has_test'] else 'Нет' for i in data]  # Наличие тестового задания
        date_of_publication = [i['published_at'][:10] for i in data]  # Дата публикации
        url = [i['alternate_url'] for i in data]  # Ссылка на вакансию

        with open(filename, 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            for nm, sal, tst, date, emp, ur in zip(name, salary, test, date_of_publication, employer, url):
                flatten = nm, sal, tst, date, emp, ur
                writer.writerow(flatten)

def main():
    keyword = input('Введите профессию/должность/компанию: ')
    get_vacansies(keyword)


if __name__ == '__main__':
    main()
