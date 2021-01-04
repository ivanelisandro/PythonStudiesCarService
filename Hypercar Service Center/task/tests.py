from functools import partial
from urllib.error import URLError
from urllib.request import urlopen
from hstest.check_result import CheckResult
from hstest.test_case import TestCase
from hstest.django_test import DjangoTest


class HypercarOperatorMenuTest(DjangoTest):

    def get_ticket(self, service: str, content: str, helper_msg: str) -> CheckResult:
        try:
            page = self.read_page(f'http://localhost:{self.port}/get_ticket/{service}')
            if content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {content} on /get_ticket/{service} page after\n'
                    f'{helper_msg}'
                )
        except URLError:
            return CheckResult.false(
                f'Cannot connect to the /get_ticket/{service} page.'
            )

    def check_menu(self, service: str, content: str, menu_content: str,
                   helper_msg: str) -> CheckResult:
        try:
            result = self.get_ticket(service, content, helper_msg)
            if not result.result:
                return result

            page = self.read_page(f'http://localhost:{self.port}/processing')
            if menu_content in page:
                return CheckResult.true()
            else:
                return CheckResult.false(
                    f'Expected to have {menu_content} on /processing page after\n'
                    f'{helper_msg}'
                )
        except URLError:
            return CheckResult.false(
                f'Cannot connect to the /processing page.'
            )

    def generate(self):
        helper_msg_1 = '\tClient #1 get ticket for inflating tires\n'
        helper_msg_2 = helper_msg_1 + '\tClient #2 get ticket for changing oil\n'
        helper_msg_3 = helper_msg_2 + '\tClient #3 get ticket for changing oil\n'
        helper_msg_4 = helper_msg_3 + '\tClient #4 get ticket for inflating tires\n'
        helper_msg_5 = helper_msg_4 + '\tClient #5 get ticket for diagnostic\n'
        return [
            TestCase(attach=self.check_server),
            TestCase(attach=partial(
                self.check_menu,
                'inflate_tires',
                'Please wait around 0 minutes',
                'Inflate tires queue: 1',
                helper_msg_1
            )),
            TestCase(attach=partial(
                self.check_menu,
                'change_oil',
                'Please wait around 0 minutes',
                'Change oil queue: 1',
                helper_msg_2
            )),
            TestCase(attach=partial(
                self.check_menu,
                'change_oil',
                'Please wait around 2 minutes',
                'Change oil queue: 2',
                helper_msg_3
            )),
            TestCase(attach=partial(
                self.check_menu,
                'inflate_tires',
                'Please wait around 9 minutes',
                'Inflate tires queue: 2',
                helper_msg_4
            )),
            TestCase(attach=partial(
                self.check_menu,
                'diagnostic',
                'Please wait around 14 minutes',
                'Get diagnostic queue: 1',
                helper_msg_5
            )),
        ]

    def check(self, reply, attach):
        return attach()


if __name__ == '__main__':
    HypercarOperatorMenuTest('hypercar.manage').run_tests()
