import unittest
import plot as plot

class plotTest(unittest.TestCase):
    def test_plotWClayer(self):

        absSorucePath = r'D:\yk_research\AquaCrop-Irrigation-Design\output\test.csv'

        plot.plotWClayer(absSorucePath)

if __name__ == '__main__':
    unittest.main()