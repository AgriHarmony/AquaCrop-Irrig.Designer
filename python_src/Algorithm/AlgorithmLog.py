from Configuration import ConfigHolder
from pathlib import Path

cfgHolder = ConfigHolder()
config = cfgHolder.get()


class AlgorithmLog():

    def __init__(self):
        self.header = self.initilizeHeader()
        self.logLines = []

    def initilizeHeader(self):
        iterativeNumber = config["compartment_num"] + 1
        WCsList = ["WC{}".format(i) for i in range(1, iterativeNumber)]
        refList = ["Ref{}".format(i) for i in range(1, iterativeNumber)]
        errLisit = ["Err{}".format(i) for i in range(1, iterativeNumber)]
        pidKpsList = ["pidkp{}".format(i) for i in range(1, iterativeNumber)]
        pidKisList = ["pidki{}".format(i) for i in range(1, iterativeNumber)]
        pidKdsList = ["pidkd{}".format(i) for i in range(1, iterativeNumber)]
        header = ["dayCount"] + WCsList + refList + errLisit +\
            pidKpsList + pidKisList + pidKdsList + ["sensor0_depth",
                                                    "sensor1_depth",
                                                    "Irri", "CC", "Biomass"]
        return header

    def getHeader(self):
        return self.header

    def display(self):
        print(self.logLines)

    def get(self):
        return self.logLines

    def log(self, logDict):

        WCsStr = ",".join(map(str, logDict["WCs"]))
        refsStr = ",".join(map(str, logDict["refs"]))
        errorsStr = ",".join(map(str, logDict["error"]))
        pidkpStr = ",".join(map(str, logDict["pidk"][0]))
        pidkiStr = ",".join(map(str, logDict["pidk"][1]))
        pidkdStr = ",".join(map(str, logDict["pidk"][2]))
        logList = []
        logList.append(logDict["dayCount"])
        logList.append(WCsStr)
        logList.append(refsStr)
        logList.append(errorsStr)
        logList.append(pidkpStr)
        logList.append(pidkiStr)
        logList.append(pidkdStr)
        logList.append(logDict["sensor0_depth"])
        logList.append(logDict["sensor1_depth"])
        logList.append(logDict["irri"])
        logList.append(logDict["CC"])
        logList.append(logDict["Biomass"])
        self.logLines.append(",".join(map(str, logList)))

    def writeLogToCSV(self, algInfo, summary, simulationName):

        logCSVdestPath = str(
            Path(config['path_prefix']['output'] + r'{}_log.csv'.format(
                simulationName)).resolve())

        with open(logCSVdestPath, 'w') as f:

            # algorthim info
            f.write("sensor0 moving:{},sensor1 moving:{},ref0:{},ref1:{}"
                    .format(
                        algInfo["sensor0"], algInfo["sensor1"],
                        algInfo["ref0"], algInfo["ref1"]
                    ) + "\n")
            # write yield/water summary
            f.write("yield:{},water:{}".format(
                summary["yield"], summary["water"]) + "\n")

            # write header
            f.write(",".join(self.header) + "\n")

            # write Log content
            for line in self.logLines:
                f.write(line + "\n")
