from parsers.parser import Parser

from bs4 import BeautifulSoup


class HtmlParser(Parser):

    def parse(self, data):
        """
        Parses html text and extracts field values
        :param data: html text (page)
        :return: a dictionary where key is one
        of defined fields and value is this field's value
        """
        soup = BeautifulSoup(data, "html.parser")

        # Your code here: find an appropriate html element
        html_goods = soup.find('div', {'id': 'productsSection'}).findChildren(recursive=False)
        goods = []
        for good in html_goods:
            model = good.get('data-model')
            date = good.get('data-release-date')
            sizes = good.get('data-sizes')
            good_button_tag = good.find('div', {'class': 'product-colors'}).findChildren(recursive=False)
            for size in sizes.split(','):
                for button in good_button_tag:
                    goods.append({self.fields[0]: model, self.fields[1]: date, self.fields[2]: size,
                                  self.fields[3]: button.get('data-standard-price'),
                                  self.fields[4]: button.get('data-promo-price'),
                                  self.fields[5]: button.find('img').get('alt')})
        return goods

    def merge(self, page_a, page_b):
        """
        merge html pages with goods into one page
        :param page_a: first html text (page)
        :param page_b: second html text (page)
        :return: a merged table in html format
        """
        soup = BeautifulSoup(page_a, "html.parser")
        base_goods = soup.find('div', {'id': 'productsSection'})
        soup = BeautifulSoup(page_b, "html.parser")
        goods_to_add = soup.find('div', {'id': 'productsSection'}).findChildren(recursive=False)

        for good in goods_to_add:
            base_goods.append(good)
        return base_goods
