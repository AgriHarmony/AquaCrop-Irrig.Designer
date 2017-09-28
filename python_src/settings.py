
class ConfigHolder():
    config = {
            "controller_coefficient": {
                "kp":1.5,
                "ki":1,
                "kd":1
            },
            "path_help": "all the path prefix is relative to python_src directory",
            
            "path_prefix": {
                "root": r'D:\yk_research\AquaCrop-Irrigation-Design',
                "input": r'../input/',
                "output": r'../output/',
                "dotPRO": r'../dotPROfiles/',
                "AC_plugin_LIST": r'../bin/aquacrop_plug_in_v5_0/LIST/',# .PRO location
                "AC_plugin_OUTP": r'../bin/aquacrop_plug_in_v5_0/OUTP/',# day and season output location
                "AC_DATA": r'../bin/aquacrop_v5_0/DATA/' #  .Irr file and input soil, climate, crop ...etc  location
            },
            "executable_path": \
                r'D:\yk_research\AquaCrop-Irrigation-Design\bin\aquacrop_plug_in_v5_0\ACsaV50.exe',
            "day_data_index": {
                "DAP": 3,
                "rain": 6,
                "irrigation": 7,
                "ET": 21,
                "zoot": 24,
                "WCtotal": 41,  # check Aquacrop plugin user manual p13 columns 44~53 
                "wc1": 62,
                "wc8": 69,
            },
            "day_data_format": {
                "COLUMN_INFO_LINE_NUM": 1,
                "COLUMN_SKIP_LINE_NUM":  2,
                "COLUMN_NAME_LINE_NUM": 3,
                "COLUMN_UNIT_LINE_NUM": 4,
                "HEADER_ROW_NUM": 4,
                "missingUnits": ['d','m','y','d','none']
            },
            "season_data_format": {
                "COLUMN_INFO_LINE_NUM": 1,
                "COLUMN_SKIP_LINE_NUM":  2,
                "COLUMN_NAME_LINE_NUM": 3,
                "COLUMN_UNIT_LINE_NUM": 4,
                "HEADER_ROW_NUM": 4,
                "missingUnits": ['d','m','y','d']
            },
            "compartmentBoundary": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    }
    def get(self):
        return self.config

