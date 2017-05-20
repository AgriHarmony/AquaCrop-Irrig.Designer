import unittest
import helper as helper

class helperTest(unittest.TestCase):
    def test_write_align_csv(self):
        absSorucePath = r'D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_plug_in_v5_0\OUTP\TOMATO2PROday.OUT'
        absDestPath = r'D:\yk_research\AquaCrop-Irrigation-Design\output\test.csv'

        helper.writeDayData2AlignedCSV(absSorucePath,absDestPath)

if __name__ == '__main__':
    unittest.main()