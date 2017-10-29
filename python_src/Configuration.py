
class ConfigHolder():
    def __init__(self):
        self.config = {
            "controller_coefficient": {
                "kp": 1.5,
                "ki": 1,
                "kd": 1
            },
            "path_help": "all the path prefix is relative to python_src directory",
            "compartment_boundary_list": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
            "compartment_num": 10,
            "path_prefix": {
                "root": r'D:\yk_research\AquaCrop-Irrigation-Design',
                "input": r'../input/',
                "output": r'../output/',
                "dotPRO": r'../dotPROfiles/',
                "AC_plugin_LIST": r'../bin/aquacrop_plug_in_v5_0/LIST/',  # .PRO location
                # day and season output location
                "AC_plugin_OUTP": r'../bin/aquacrop_plug_in_v5_0/OUTP/',
                # .Irr file and input soil, climate, crop ...etc  location
                "AC_DATA": r'../bin/aquacrop_v5_0/DATA/'
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
                "wc10": 72,
            },
            "day_data_format": {
                "COLUMN_INFO_LINE_NUM": 1,
                "COLUMN_SKIP_LINE_NUM":  2,
                "COLUMN_NAME_LINE_NUM": 3,
                "COLUMN_UNIT_LINE_NUM": 4,
                "HEADER_ROW_NUM": 4,
                "missingUnits": ['d', 'm', 'y', 'd', 'none']
            },
            "season_data_format": {
                "COLUMN_INFO_LINE_NUM": 1,
                "COLUMN_SKIP_LINE_NUM":  2,
                "COLUMN_NAME_LINE_NUM": 3,
                "COLUMN_UNIT_LINE_NUM": 4,
                "HEADER_ROW_NUM": 4,
                "missingUnits": ['d', 'm', 'y', 'd']
            },
            "csv_day_data_column_string": ('Day	Month	Year	DAP	Stage	WC(1.20)	Rain	Irri	'
                                           'Surf	Infilt	RO	Drain	CR	Zgwt	Ex	E	E/Ex	'
                                           'Trx	Tr	Tr/Trx	ETx	ET	ET/ETx	GD	Z	StExp	StSto	'
                                           'StSen	StSalt	CC	Kc(Tr)	Trx	Tr	Tr/Trx	WP	StBio	'
                                           'Biomass	HI	Yield	Brelative	WPet	WC(1.20)	Wr(1.00)'
                                           '	Z	Wr	Wr(SAT)	Wr(FC)	Wr(exp)	Wr(sto)	Wr(sen)	Wr(PWP)	'
                                           'SaltIn	SaltOut	SaltUp	Salt(1.20)	SaltZ	Z	ECe	ECsw	'
                                           'StSalt	Zgwt	ECgw	WC1	WC2	WC3	WC4	WC5	WC6	WC7	WC8	WC9	WC10'
                                           '	WC11	WC12	ECe1	ECe2	ECe3	ECe4	ECe5	ECe6'
                                           '	ECe7	ECe8	ECe9	ECe10	ECe11	ECe12	Rain	ETo	Tmin	Tavg	Tmax	CO2'),

            "csv_season_data_column_string": ('Period	Day1	Month1	Year1	Rain	ETo	GD	CO2	Irri	'
                                              'Infilt	Runoff	Drain	Upflow	E	E/Ex	Tr	Tr/Trx	SaltIn	'
                                              'SaltOut	SaltUp	SaltProf	Cycle	SaltStr	FertStr	TempStr	'
                                              'ExpStr	StoStr	BioMass	Brelative	HI	Yield	WPet	DayN	MonthN	YearN	File')
        }

    def get(self):
        return self.config

    def getCSVDayDataColumnTuple(self):
        dataString = self.config["csv_day_data_column_string"]
        dataString = dataString.replace('\n', '')
        return tuple([s.strip() for s in dataString.split('\t')])

    def getCSVSeasonDataColumnTuple(self):
        dataString = self.config["csv_season_data_column_string"]
        dataString = dataString.replace('\n', '')
        return tuple([s.strip() for s in dataString.split('\t')])
