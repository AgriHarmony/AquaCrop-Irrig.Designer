import unittest
import plot as myplot
from Configuration import ConfigHolder
from pathlib import Path


class plotTest(unittest.TestCase):

    # def test_plotWClayer(self):

    #     absSorucePath = r'D:\yk_research\AquaCrop-Irrigation-Design\output\test.csv'
    #     myplot.plotWClayer(absSorucePath)

    def test_plot_WC_layers(self):

        csvFileName = "depth0_ref35_moving_15_day.csv"
        configHolder = ConfigHolder()
        config = configHolder.get()
        prefixOutput = config['path_prefix']['output']

        path = str(Path(prefixOutput + csvFileName).resolve())
        myplot.plot_WC_layers(path)


if __name__ == '__main__':
    unittest.main()
