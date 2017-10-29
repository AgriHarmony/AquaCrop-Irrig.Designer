import unittest
import helper as helper
from Configuration import ConfigHolder
from pathlib import Path
configHolder = ConfigHolder()
config = configHolder.get()


class helperTest(unittest.TestCase):

    def test_write_align_csv(self):
        absSorucePath = r'D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_plug_in_v5_0\OUTP\TOMATO2PROday.OUT'
        absDestPath = r'D:\yk_research\AquaCrop-Irrigation-Design\output\test.csv'

        helper.writeDayData2AlignedCSV(absSorucePath, absDestPath)

    def test_read_shared_data(self):

        # print("test_read_shared_data")

        path = r'D:\yk_research\AquaCrop-Irrigation-Design\output\moving_control_point\shared_info.json'
        # print(helper.readSharedInfo(path))

    def test_increase_id_shared_info(self):

        # print("test_increase_id_shared_info")

        path = r'D:\yk_research\AquaCrop-Irrigation-Design\output\moving_control_point\shared_info.json'
        nextId = helper.readSharedInfo(path)["current_unique_id"] + 1
        # print(nextId)

        helper.increaseIdSharedInfo(path)
        currentId = helper.readSharedInfo(path)["current_unique_id"]
        self.assertEqual(nextId, currentId)

    def test_loadDayCSV(self):

        csvSourceFile = r"D:\yk_research\AquaCrop-Irrigation-Design\output\data_for_test\depth1_ref30_day.csv"
        helper.loadDayCSV(csvSourceFile)

    def test_loadSeasonCSV(self):

        csvSourceFile = r"D:\yk_research\AquaCrop-Irrigation-Design\output\data_for_test\depth1_ref30_season.csv"
        helper.loadSeasonCSV(csvSourceFile)


if __name__ == '__main__':

    unittest.main()
