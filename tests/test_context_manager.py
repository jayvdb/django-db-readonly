from django.db import transaction
from django.db.transaction import TransactionManagementError

from django.test import TestCase

from readonly.decorators import readonly, write_enabled
from readonly.exceptions import DatabaseWriteDenied

from tests.models import Widget


class ContextManagerTestCase(TestCase):
    def _create_obj(self):
        with transaction.atomic():
            obj = Widget.objects.create()
            obj.save()

    def test_normal(self):
        Widget.objects.count()
        obj = Widget.objects.create()
        obj.save()

    def test_readonly_transaction(self):
        before = Widget.objects.count()

        with readonly():
            with self.assertRaises(DatabaseWriteDenied):
                with transaction.atomic():
                    obj = Widget.objects.create()
                    obj.save()

        after = Widget.objects.count()
        assert after == before

        obj = Widget.objects.create()
        obj.save()

        after = Widget.objects.count()
        assert after == before + 1

    def test_readonly(self):
        Widget.objects.count()

        with readonly():
            with self.assertRaises(DatabaseWriteDenied):
                obj = Widget.objects.create()
                obj.save()

        # TODO: Automatic cancellation of the transaction would simplify
        # developer use of readonly & DatabaseWriteDenied with foreign code
        with self.assertRaises(TransactionManagementError):
            Widget.objects.count()

    def test_nested_readonly_disabled(self):
        with readonly():
            with self.assertRaises(DatabaseWriteDenied):
                self._create_obj()
            with readonly():
                with self.assertRaises(DatabaseWriteDenied):
                    self._create_obj()
                with readonly():
                    with self.assertRaises(DatabaseWriteDenied):
                        self._create_obj()

        Widget.objects.create()

    def test_readonly_enabled(self):
        with readonly():
            with write_enabled():
                self._create_obj()

    def test_nested_readonly_enabled(self):
        with readonly():
            with readonly():
                with write_enabled():
                    with readonly():
                        with write_enabled():
                            with readonly():
                                with self.assertRaises(DatabaseWriteDenied):
                                    self._create_obj()

                with self.assertRaises(DatabaseWriteDenied):
                    self._create_obj()

            with self.assertRaises(DatabaseWriteDenied):
                self._create_obj()

        self._create_obj()
