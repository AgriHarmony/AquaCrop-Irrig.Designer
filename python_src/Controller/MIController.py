import time


class MIController():

    def __init__(self, ref1=25, ref2=10):

        self.ref1 = ref1
        self.ref2 = ref2

        self.kp = 0.0
        self.kp2 = 0.0
        self.ki = 0.0
        self.kd = 0.0

        self.pterm = 0
        self.iterm = 0
        self.dterm = 0

        self.tuningFactor = 0.1

        self.e1 = 0.0
        self.e2 = 0.0

        self.last_time = 0
        self.delta_time = 1
        self.sample_time = 1

        self.output = 0

        self.stateRecord = []
        self.stateK1 = []
        self.stateK2 = []
        self.stateDefintion = ['shallow dry, deeper dry', 'shallow, dry, deeper, wet',
                               'shallow, wet, deeper, wet', 'shallow, dry, deeper, wet']

    def setK(self, kp, kp2, ki, kd):

        self.kp = kp
        self.kp2 = kp2
        self.ki = ki
        self.kd = kd

    def updateWithAdaptive(self, wc1, wc2, rain, simuDay):
        pass
        
    def update3Point(self, wc_shallow1, wc_shallow2, wc_deep, rain, simuDay):
        pass

    def update(self, wc_shallow, wc_deep, rain, simuDay):

        self.e1 = self.ref1 - wc_shallow 
        self.e2 = self.ref2 - wc_deep  
       
        e1 = self.e1
        e2 = self.e2

        error = 0

    
        # Problem: Should I combine to e1 and e2 into single error ?
        ##  shallow dry, deeper dry
        if e1 > 0 and e2 > 0:

            self.stateRecord.append(0)
            self.output = e1 * self.kp

        ## shallow dry, deeper wet
        elif e1 > 0 and e2 < 0:

            self.stateRecord.append(1)
            self.output = e1 * self.kp

        ## hallow wet, deeper wet, over-irrigation state
        elif e1 < 0 and e2 < 0:

            self.stateRecord.append(2)
            print()
            # self.kp = self.kp + self.tuningFactor
            self.output = e1 * self.kp + e2 * self.kp2

        ## shallow wet, deeper dry
        elif e1 < 0 and e2 > 0:

            self.stateRecord.append(3)
            if rain > 0:
                # if yesterday is rainy, just wait infl process to output water
                # in shallow
                self.output = 0
            else:
                # self.kp = self.kp - self.tuningFactor
                self.output = 0

    def get_error1(self):
        return self.e1

    def get_error2(self):
        return self.e2

    def get_output(self):
        return self.output

    def get_state(self, simuDay):

        print("simuDay:{}".format(simuDay))
        print(self.stateRecord[simuDay-1])
        stateCode = self.stateRecord[simuDay-1]
        if stateCode in [0, 1, 2, 3]: 
            return self.stateDefintion[stateCode]
        else:
            pass
