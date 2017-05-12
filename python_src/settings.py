
class ConfigHolder():
    config = {
            "controller_coefficient": {
                "kp":1.5,
                "ki":1,
                "kd":1
            },
            "path_help": "all the path prefix is relative to python_src directory",
            
            "path_prefix": {
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
                "zoot": 24,
                "wc1": 62,
                "wc2": 63,
                "rain": 6,
                "irrigation": 7
            },
            "compartmentBoundary": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    }
    def get(self):
        return self.config

