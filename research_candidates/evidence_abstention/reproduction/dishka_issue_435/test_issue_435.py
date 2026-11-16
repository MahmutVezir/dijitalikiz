"""Minimal stdlib-only regression reproducer for reagento/dishka#435."""
import unittest

from dishka import Provider, Scope, make_container, provide


class RealProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_int(self) -> int:
        return 1


class FakeProvider(Provider):
    @provide(scope=Scope.APP)
    def get_int(self) -> int:
        return 42


class Interactor:
    def __init__(self, dep: int) -> None:
        self.dep = dep

    def __call__(self) -> int:
        return self.dep


class ServiceProvider(Provider):
    get_interactor = provide(Interactor, scope=Scope.REQUEST)


class Issue435Regression(unittest.TestCase):
    def test_issue_435_override_lower_scope(self) -> None:
        container = make_container(
            RealProvider(),
            ServiceProvider(),
            FakeProvider(),
        )
        with container() as request_container:
            service = request_container.get(Interactor)
            self.assertEqual(service(), 42)


if __name__ == "__main__":
    unittest.main()
