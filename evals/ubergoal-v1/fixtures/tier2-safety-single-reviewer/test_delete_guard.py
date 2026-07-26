import unittest

from delete_guard import require_actor


class DeleteGuardTest(unittest.TestCase):
    def test_missing_actor_refused(self):
        with self.assertRaises(ValueError):
            require_actor(None)

    def test_configured_actor_preserved(self):
        self.assertEqual("operator-7", require_actor("operator-7"))
