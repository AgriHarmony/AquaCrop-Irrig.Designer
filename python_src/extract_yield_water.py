from os import listdir
from os.path import isfile, join, basename
from pathlib import Path
from Configuration import ConfigHolder
import linecache

if __name__ == "__main__":
    config = ConfigHolder().get()

    targetFolder = "ref_moving"
    # list target folder to get all file  then  generate a list  is .csv and
    # log file
    targetPathStr = config['path_prefix']['output'] + "/" + targetFolder
    outputPath = Path(targetPathStr).resolve()
    logCSVList = [f for f in listdir(
        outputPath) if isfile(join(outputPath, f)) and f.split(".")[1] == "csv"
        and f.split(".")[0].split("_")[-1] == "log"]
    # print(logCSVList)

    resultList = {}
    #  loop iterate all list to read yield and water
    for f in logCSVList:

        filePath = Path(targetPathStr + '/' + f).resolve()
        with open(filePath, "r") as fp:
            lines = fp.readlines()
            nameSeg = f.split("_")
            ref = nameSeg[0]
            mp = nameSeg[1]

            result = lines[1].split(",")
            y = result[0].split(":")[1]
            w = result[1].split(":")[1]
            index = "{}{}".format(ref, mp)
            resultList[index] = "{},{},{},{}".format(ref, mp, y, w)
        # resultLine = linecache.getline(filePath, 1)
        #  write to a common list

    #  end the loop
    result.sort()
    print(resultList)
    outPath = config['path_prefix']['output'] + "/extract_results.csv"

    moving_presentage = ["09", "08", "07", "06", "05", "04", "03", "02", "01"]
    references = list(range(25, 36))
    with open(Path(outPath).resolve(), "w") as fout:
        fout.write("ref,mp(%),yield,water\n")
        for mp in moving_presentage:
            for ref in references:
                index = "{}ref{}mp".format(str(ref), mp)
                fout.write(resultList[index])
                # for elem in resultList:
                #     fout.write(elem)
