import unittest

from dftinpgen.utils import get_elem_symbol
from dftinpgen.utils import DftinpgenUtilsError


class TestUtils(unittest.TestCase):
    """Unit test for helper utilities in :mod:`dftinpgen.utils`."""

    def test_get_elem_symbol(self):
        self.assertEqual(get_elem_symbol('Fe-34'), 'Fe')
        self.assertEqual(get_elem_symbol('3RGe-34'), 'Ge')
        with self.assertRaises(DftinpgenUtilsError):
            print(get_elem_symbol('G23'))


if __name__ == '__main__':
    unittest.main()
