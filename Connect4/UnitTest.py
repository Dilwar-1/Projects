import unittest
from Connect4Version3 import *

class Test_Connect4(unittest.TestCase):

    def setUp(self):
        self.empty_grid = init_grid()
        self.x_token = X()
        self.o_token = O()

    def test_init_grid(self):
        grid = init_grid()
        self.assertIsInstance(grid, tuple)
        self.assertEqual(len(grid), 7)
        for col in grid:
            self.assertIsInstance(col, tuple)
            self.assertEqual(len(col), 6)
            for cell in col:
                self.assertIsNone(cell)

    def test_place_token_in_column(self):
        col = (None, None, None, None, None, None)
        new_col = place_token_in_column(col, self.x_token)
        expected_col = (None, None, None, None, None, X())
        self.assertEqual(new_col, expected_col)

        col = (None, None, None, None, None, X())
        new_col = place_token_in_column(col, self.o_token)
        expected_col = (None, None, None, None, O(), X())
        self.assertEqual(new_col, expected_col)

        col = (X(), X(), X(), X(), X(), X())
        new_col = place_token_in_column(col, self.o_token)
        self.assertIsNone(new_col)

    def test_check_for_winner(self):
        grid = (
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (X(), X(), X(), X(), None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None)
        )
        self.assertTrue(check_for_winner(grid, self.x_token))

        grid = (
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (O(), O(), O(), O(), None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None)
        )
        self.assertTrue(check_for_winner(grid, self.o_token))

        grid = (
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (O(), O(), None, O(), None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None),
            (None, None, None, None, None, None)
        )
        self.assertFalse(check_for_winner(grid, self.o_token))

    def test_check_for_draw(self):
        grid = (
            (X(), O(), X(), O(), X(), O()),
            (O(), X(), O(), X(), O(), X()),
            (X(), O(), X(), O(), X(), O()),
            (O(), X(), O(), X(), O(), X()),
            (X(), O(), X(), O(), X(), O()),
            (O(), X(), O(), X(), O(), X()),
            (X(), O(), X(), O(), X(), O())
        )
        self.assertTrue(check_for_draw(grid))

        grid = (
            (X(), O(), X(), O(), X(), None),
            (O(), X(), O(), X(), O(), X()),
            (X(), O(), X(), O(), X(), O()),
            (O(), X(), O(), X(), O(), X()),
            (X(), O(), X(), O(), X(), O()),
            (O(), X(), O(), X(), O(), X()),
            (X(), O(), X(), O(), X(), O())
        )
        self.assertFalse(check_for_draw(grid))

    def test_parse_token(self):
        self.assertEqual(parse_token("x"), X())
        self.assertEqual(parse_token("o"), O())
        self.assertIsNone(parse_token("invalid"))

if __name__ == '__main__':
    unittest.main()
