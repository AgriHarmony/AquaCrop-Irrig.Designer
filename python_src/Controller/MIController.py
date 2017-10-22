import time
import numpy as np


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

        self.lastTime = 0
        self.deltaTime = 1
        self.sampleTime = 1

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
        # shallow dry, deeper dry
        if e1 > 0 and e2 > 0:

            self.stateRecord.append(0)
            self.output = e1 * self.kp

        # shallow dry, deeper wet
        elif e1 > 0 and e2 < 0:

            self.stateRecord.append(1)
            self.output = e1 * self.kp

        # hallow wet, deeper wet, over-irrigation state
        elif e1 < 0 and e2 < 0:

            self.stateRecord.append(2)
            print()
            # self.kp = self.kp + self.tuningFactor
            self.output = e1 * self.kp + e2 * self.kp2

        # shallow wet, deeper dry
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
        print(self.stateRecord[simuDay - 1])
        stateCode = self.stateRecord[simuDay - 1]
        if stateCode in [0, 1, 2, 3]:
            return self.stateDefintion[stateCode]
        else:
            pass


# Vectorization Implementation
class SimpleController():

    def __init__(self, soilProperityDict, soilProfile, sensorIntepret):

        self.sat = soilProperityDict["sat"]
        self.fc = soilProperityDict["fc"]
        self.pwp = soilProperityDict["pwp"]

        self.refnpArray = np.zeros((soilProfile["compartmentNum"]))
        # 3 X compartmentNum index [0,:]=>kp0, [0,:]=>ki, [0,:]=>kd
        self.knpArray = np.zeros((3, soilProfile["compartmentNum"]))
        self.errornpArray = np.zeros((soilProfile["compartmentNum"]))
        self.controlDepth = sensorIntepret['controlDepth']

        self.kArrayIndexpIndex = {'p': 0, 'i': 1, 'd': 2}

        # PID computing variables
        self.sampleTime = 0.00
        self.currentTime = time.time()
        self.lastTime = self.currentTime
        self.lastError = np.zeros((soilProfile["compartmentNum"]))
        self.PIDTermArray = np.zeros((3, soilProfile["compartmentNum"]))
        self.windupGuard = 20.0

    def get_ref(self):
        return self.refnpArray

    def set_ref(self, refArray):
        self.refnpArray = refArray

    def get_kArray_index(self):
        return self.kArrayIndexpIndex

    def get_k(self):
        return self.knpArray

    def set_k(self, kArray):
        self.knpArray = kArray

    def get_output(self, WCsnpArray):

        self.errornpArray = self.refnpArray - WCsnpArray
        # print("in get_output, controlDepth={}".format(self.controlDepth))
        irri = self.pid_update(
            self.refnpArray[self.controlDepth], WCsnpArray[self.controlDepth], self.controlDepth)
        # irri = self.errornpArray.dot(self.knpArray[self.kArrayIndexpIndex['p']])
        return irri

    def set_controlDepth(self, newControlDepth):
        self.controlDepth = newControlDepth

    def get_error(self, WCsnpArray):
        return self.refnpArray - WCsnpArray

    def pid_update(self, ref, feedbackValue, depth):
        """Calculates PID value for given reference feedback

        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}

        .. figure:: images/pid_1.png
           :align:   center

           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)

        """

        error = ref - feedbackValue
        Kp = self.knpArray[self.kArrayIndexpIndex['p'], depth]
        Ki = self.knpArray[self.kArrayIndexpIndex['i'], depth]
        Kd = self.knpArray[self.kArrayIndexpIndex['d'], depth]
        # print("In pid_update ref:{}".format(ref))
        # print("In pid_update Kp:{}, Ki:{}, Kd:{}".format(Kp,Ki,Kd))
        self.currentTime = time.time()
        deltaTime = self.currentTime - self.lastTime
        deltaError = error - self.lastError[depth]
        ITerm = self.PIDTermArray[self.kArrayIndexpIndex['i'], depth]

        if (deltaTime >= self.sampleTime):
            PTerm = Kp * error
            # print("Pterm:{}".format(str(PTerm)))
            ITerm += error * deltaTime
            if (ITerm < -self.windupGuard):
                ITerm = -self.windupGuard
            elif (ITerm > self.windupGuard):
                ITerm = self.windupGuard
            # print("ITerm:{}".format(str(ITerm)))
            DTerm = 0.0
            if deltaTime > 0:
                DTerm = deltaError / deltaTime
            # print("DTerm:{}".format(str(DTerm)))
            # Remember last time and last error for next calculation
            self.lastTime = self.currentTime
            self.lastError[depth] = error

            # store PID term
            self.PIDTermArray[self.kArrayIndexpIndex['i'], depth] = ITerm
            return PTerm + (Ki * ITerm) + (Kd * DTerm)

    def set_windup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windupGuard = windup

    def get_status(self, WCs):

        pass
        # return {'e': [ e0, e1, e2, e3], 'ref': [self.ref0, self.ref1, self.ref2, self.ref3], \
        #     'k': [self.k0, self.k1, self.k2, self.k3]}
