#Рекуррентный
class DeltaPIDRegulator:
    P = 0
    I = 0
    D = 0
    Dt = 0

    maxOutput = 0
    minOutput = 0
    errorSum = 0
    maxError = 0
    lastOutput = 0
    lastError = 0
    last2Error = 0
    maxOutputRampRate = 0

    def __init__(self, p: float, ti: float, d: float, dt: float):
        self.P = p
        self.I = ti
        self.D = d
        self.Dt = dt

    def setOutputLimits(self, minimum, maximum):
        if maximum < minimum:
            return
        self.maxOutput = maximum
        self.minOutput = minimum

    def setMaxOutputRampRate(self, rate):
        self.maxOutputRampRate = rate

    def getOutput(self, actual, setpoint):
        error = setpoint - actual
        q0 = self.P + self.I * self.Dt + self.D / self.Dt
        q1 = -self.P - 2 * self.D / self.Dt
        q2 = self.D / self.Dt
        output = q0 * error + q1 * self.lastError * q2 * self.last2Error
        output = self.constrain(output, self.minOutput, self.maxOutput)
        if self.maxOutputRampRate != 0:
            output = self.constrain(output, self.lastOutput-self.maxOutputRampRate, self.lastOutput+self.maxOutputRampRate)

        self.last2Error = self.lastError
        self.lastError = error
        self.lastOutput = output
        return output;

    def constrain(self, value, min, max):
        if value > max:
            return max
        if value < min:
            return min
        return value
