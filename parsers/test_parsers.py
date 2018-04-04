import unittest

from parsers.filter_parser import FilterParser
from parsers.html_parser import HtmlParser
from storages.file_storage import FileStorage


class TestFilterParser(unittest.TestCase):
    def test_parse(self):
        parser = FilterParser(['1', '3', '5'])
        parsed_data = parser.parse({'1': 1, '2': 2, '3': 3, '4': 4, '5': 5})
        self.assertEqual(len(parsed_data), 1)
        self.assertDictEqual(parsed_data[0], {'1': 1, '3': 3, '5': 5})


class TestHtmlParser(unittest.TestCase):

    def test_parse(self):
        # init data and parser
        parser = HtmlParser(['model', 'date', 'size', 'standard-price', 'promo-price', 'color'])
        storage = FileStorage('../test_data.html')

        # read data from storage
        text = ''
        for i in storage.read_data():
            text += i

        # parse and check
        parsed_data = parser.parse(text)
        self.assertEqual(len(parsed_data), 5296)

    def test_merge(self):
        # init storage and parser for merging
        parser = HtmlParser([])
        storage = FileStorage('../file1.html')
        text_a = ''
        for i in storage.read_data():
            text_a += i

        storage = FileStorage('../file2.html')
        text_b = ''
        for i in storage.read_data():
            text_b += i

        # merge two pages into one
        parsed_data = parser.merge(text_a, text_b)
        storage = FileStorage('../result.html')
        storage.write_data(['goods table\t' + str(parsed_data).replace('\n', '')])
        # self.assertEqual(len(parsed_data), 5296)


if __name__ == '__main__':
    unittest.main()
