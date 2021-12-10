class PReg:
    P = 0
    D = 0
    I = 0
    setpoint = 0
    eastActual = 0
    maxOutput = 0
    minOutput = 0
    errorSum = 0
    maxError = 0
    lastOutput = 0
    maxOutputRampRate = 0

    def __init__(self, p: float, d: float, i: float):
        self.P = p
        self.D = d
        self.I = i

    def setOutputLimits(self, minimum: float, maximum: float):
        if maximum < minimum:
            return
        self.maxOutput = maximum
        self.minOutput = minimum

    def getOutput(self, actual: float, setpoint: float):
        error = setpoint - actual
        Poutput = error
        if self.Bounded(self.lastOutput, self.minOutput, self.maxOutput):
            self.errorSum += error
            self.maxError = self.errorSum
        else:
            self.errorSum = self.maxError
        Ioutput = self.I * self.errorSum
        Doutput = self.D * (actual - self.eastActual)
        self.eastActual = actual
        output = self.P * (Poutput + Doutput + Ioutput)
        output = self.constrain(output, self.minOutput, self.maxOutput)
        if self.maxOutputRampRate != 0:
            output = self.constrain(output - self.lastOutput,
                                    self.eastActual - self.maxOutputRampRate,
                                    self.eastActual + self.maxOutputRampRate)
            self.lastOutput = output
        return output

    def setMaxOutputRampRate(self, rate):
        self.maxOutputRampRate = rate

    def constrain(self, value: float, min: float, max: float):
        if value > max:
            return max
        if value < min:
            return min
        return value

    def Bounded(self, value: float, min: float, max: float):
        return min < value and max > value
