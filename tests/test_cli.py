import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from backend import sortowanie
from cli import main, sort_menu


class CliTests(unittest.TestCase):
    def test_sort_menu_reports_selected_algorithm(self):
        sorter = sortowanie()
        sorter.data = [3, 1, 2]
        output = io.StringIO()

        with patch("cli.wait_for_key"), redirect_stdout(output):
            sort_menu("4", sorter)

        self.assertEqual(sorter.get_data(), [1, 2, 3])
        self.assertIn("Bubble Sorted items: [1, 2, 3]", output.getvalue())

    def test_main_can_add_clear_and_exit(self):
        output = io.StringIO()
        choices = iter(["1", "8", "3", "8"])

        with patch("builtins.input", side_effect=lambda _prompt: next(choices)), redirect_stdout(output):
            main()

        self.assertIn("Added: 8", output.getvalue())
        self.assertIn("Exiting...", output.getvalue())


if __name__ == "__main__":
    unittest.main()