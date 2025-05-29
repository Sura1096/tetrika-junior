"""
Необходимо реализовать скрипт, который будет получать с русскоязычной википедии
список всех животных (https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту)
и записывать в файл в формате beasts.csv количество животных на каждую букву алфавита.
Содержимое результирующего файла:
А,642
Б,412
В,...

Примечание:
анализ текста производить не нужно, считается любая запись
из категории (в ней может быть не только название, но и, например, род)
"""
import csv

from bs4 import BeautifulSoup
import requests


BASE_URL = f'https://ru.wikipedia.org'
START_URL = ('/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F'
             ':%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_'
             '%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&from=%3Cb%3E%D0%90%3C%2Fb%3E')


def get_next_page(soup: BeautifulSoup) -> str | None:
    next_page_url = soup.find(id='mw-pages').find('a', string='Следующая страница')
    if next_page_url:
        return BASE_URL + next_page_url.get('href')
    return None


def get_animal_amount() -> list[tuple[str, int]]:
    next_page = BASE_URL + START_URL
    syl_dict = {}

    while next_page:
        page = requests.get(next_page)
        page.raise_for_status()
        soup = BeautifulSoup(page.text, 'lxml')
        animals = (soup.find(class_='mw-category mw-category-columns')
                   .find_all(class_='mw-category-group'))

        for item in animals:
            syl = item.find('h3').text.strip()
            items = item.find_all('li')
            syl_dict[syl] = syl_dict.get(syl, 0) + len(items)
        next_page = get_next_page(soup)

    return sorted(syl_dict.items())


def write_to_csv(
        data: list[tuple[str, int]],
        filename: str = 'beasts.csv'
) -> None:
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow(item)


def main():
    try:
        animal_amount = get_animal_amount()
        write_to_csv(animal_amount)
        print('Данные успешно записаны в beasts.csv')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    main()