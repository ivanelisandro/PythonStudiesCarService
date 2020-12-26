import re
from urllib.error import URLError
from urllib.request import urlopen
from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.django_test import DjangoTest


class HypercarClientMenuTest(DjangoTest):
    ELEMENT_PATTERN = '''<a[^>]+href=['"](?P<href>[a-zA-Z/_]+)['"][^>]*>'''

    def get_client_menu_page(self) -> CheckResult:
        try:
            page = self.read_page(f'http://localhost:{self.port}/menu')
            links = re.findall(self.ELEMENT_PATTERN, page)
            for link in (
                '/get_ticket/change_oil',
                '/get_ticket/inflate_tires',
                '/get_ticket/diagnostic',
            ):
                if link not in links:
                    return CheckResult.false(
                        f'Menu page should contain <a> element with href {link}'
                    )
            return CheckResult.true()
        except URLError:
            return CheckResult.false(
                'Cannot connect to the /menu page.'
            )

    def generate(self):
        return [
            TestCase(attach=self.check_server),
            TestCase(attach=self.get_client_menu_page),
        ]

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    HypercarClientMenuTest('hypercar.manage').run_tests()
