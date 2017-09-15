# Common
ref=25
depth=0

# P
    ku=7
    kArray[kArrayIndex['p'],depth]=0.45*ku
    kArray[kArrayIndex['i'],depth]=0
    kArray[kArrayIndex['d'],depth]=0
# PI
    ku=7
    tu=30
    kArray[kArrayIndex['p'],depth]=0.45*ku
    kArray[kArrayIndex['i'],depth]=0
    kArray[kArrayIndex['i'],depth]=0.54*ku/tu
    kArray[kArrayIndex['d'],depth]=0

   
# PI2 
    ku=4
    tu=0.7
    kArray[kArrayIndex['p'],depth]=0.45*ku
    kArray[kArrayIndex['i'],depth]=0
    kArray[kArrayIndex['i'],depth]=tu/2
    kArray[kArrayIndex['d'],depth]=0
    # kArray[kArrayIndex['d'],depth]=tu/8