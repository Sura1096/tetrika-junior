import unittest
from unittest.mock import patch, Mock

from bs4 import BeautifulSoup

from tasks.task2.solution import get_next_page, get_animal_amount, write_to_csv
from html_test_cases import (next_page_html, none_next_page_html,
                             animals_html, animals_last_html_page)


class TestTask2(unittest.TestCase):
    def test_get_next_page(self):
        soup = BeautifulSoup(next_page_html, 'lxml')
        next_page = get_next_page(soup)
        assert next_page == 'https://ru.wikipedia.org/nextLink'

    def test_get_next_page_no_link(self):
        soup = BeautifulSoup(none_next_page_html, 'lxml')
        next_page = get_next_page(soup)
        assert next_page is None

    @patch('tasks.task2.solution.requests.get')
    def test_get_animal_amount(self, mock_get):
        mock_response1 = Mock()
        mock_response1.text = animals_html
        mock_response1.raise_for_status = lambda: None

        mock_response2 = Mock()
        mock_response2.text = animals_last_html_page
        mock_response2.raise_for_status = lambda: None

        mock_get.side_effect = [mock_response1, mock_response2]

        result = get_animal_amount()

        expected = [('А', 2), ('Б', 1)]
        self.assertEqual(result, expected)

    def test_write_to_csv(self):
        import os
        data = [('А', 10), ('Б', 5)]
        filename = 'test_output.csv'

        write_to_csv(data, filename)

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn("А,10", content)
        self.assertIn("Б,5", content)

        os.remove(filename)
